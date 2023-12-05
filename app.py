from flask import Flask, url_for, jsonify, request, redirect, session, render_template
import datetime as dt
import requests, random
import sqlite3, os, bcrypt

app = Flask(__name__)
#In a non development environment change this to be a dynamic env variable
app.secret_key = '1768543'

# added for cookie security (:
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

@app.route('/')
def api_main():
    return home()



@app.route('/TestHome.html')
def home():
    return render_template('TestHome.html')

@app.route('/AboutUs.html')
def aboutus():
    return render_template('AboutUs.html')

@app.route('/PlacesToEat.html')
def PlacesToEat():
    return render_template('PlacesToEat.html')

@app.route('/Events.html')
def Events():
    return render_template('Events.html')

@app.route('/PlacesToEatOffCampus.html')
def PlacesToEatOffCampus():
    return render_template('PlacesToEatOffCampus.html')

@app.route('/PlacesToEatOnCampus.html')
def PlacesToEatOnCampus():
    return render_template('PlacesToEatOnCampus.html')

def get_db_connection():
    conn = sqlite3.connect('student_planner.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = user['id']
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'incorrect_credentials'})

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove the user ID from the session
    session.pop('user_id', None)
    # Redirect to the login page
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user:
        conn.close()
        return jsonify({'status': 'username_exists'})
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()

    # Fetch the new user's ID
    new_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    new_user_id = new_user['id']

    # Generate and insert the random schedule
    random_schedule = generate_random_schedule(new_user_id)
    conn.executemany('INSERT INTO schedule (user_id, day, start_time, end_time, class_name) VALUES (?, ?, ?, ?, ?)', random_schedule)
    conn.commit()
    conn.close()

    return jsonify({'status': 'account_created'})

def does_overlap(new_start, new_end, existing_slots):
    for start, end in existing_slots:
        if new_start < end and new_end > start:
            return True
    return False

def generate_random_schedule(user_id):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    class_names = ['Class1', 'Class2', 'Class3', 'Class4', 'Class5']
    schedule = []
    existing_slots = {day: [] for day in days}

    for class_name in class_names:
        class_days = random.sample(days, 2)  # Pick two random days for each class
        for day in class_days:
            while True:
                start_hour = random.randint(7, 19)  # Random start hour between 7 AM and 7 PM
                start_time = dt.datetime(2023, 1, 1, start_hour, random.choice([0, 15, 30, 45]))  # Random start minute
                end_time = start_time + dt.timedelta(minutes=75)  # Class duration is 1 hour and 15 minutes

                if not does_overlap(start_time, end_time, existing_slots[day]):
                    existing_slots[day].append((start_time, end_time))
                    schedule.append((user_id, day, start_time.strftime('%I:%M %p'), end_time.strftime('%I:%M %p'), class_name))
                    break

    return schedule

@app.route('/StudentPlanner.html')
def StudentPlanner():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        schedule_data = conn.execute('''
            SELECT * FROM schedule 
            WHERE user_id = ? 
            ORDER BY 
                CASE day 
                    WHEN 'Monday' THEN 1 
                    WHEN 'Tuesday' THEN 2 
                    WHEN 'Wednesday' THEN 3 
                    WHEN 'Thursday' THEN 4 
                    WHEN 'Friday' THEN 5 
                END, 
                start_time
        ''', (user_id,)).fetchall()
        conn.close()
        return render_template('StudentPlanner.html', schedule=schedule_data)
    else:
        return redirect(url_for('login'))

@app.route('/StudentResources.html')
def StudentResources():
    return render_template('StudentResources.html')

@app.route('/StudentResourcesAcademic.html')
def StudentResourcesAcademic():
    return render_template('StudentResourcesAcademic.html')

@app.route('/StudentResourcesFinancial.html')
def StudentResourcesFinancial():
    return render_template('StudentResourcesFinancial.html')

@app.route('/StudentResourcesHolistic.html')
def StudentResourcesHolistic():
    return render_template('StudentResourcesHolistic.html')

def kelvin_to_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit

def mps_to_mph(mps):
    mph = mps * 2.237
    return mph

@app.route('/Weather.html')
def Weather():
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "759cb2753beefcf28c82cafe746183ab"
    CITY = "Kent"
    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()

    if response['cod'] == 200:  
        # Temperature
        temp_kelvin = response['main']['temp']
        temp_fahrenheit = kelvin_to_fahrenheit(temp_kelvin)
        # Feels like
        feels_like_kelvin = response['main']['feels_like']
        feels_like_fahrenheit = kelvin_to_fahrenheit(feels_like_kelvin)
        # Humidity
        humidity = response['main']['humidity']
        # Weather description
        description = response['weather'][0]['description']
        # Sunrise Time
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'])
        # Sunset Time
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'])
        # Wind Speed
        wind_speed_in_mps = response['wind']['speed']
        wind_speed = mps_to_mph(wind_speed_in_mps)
    else:
        return "Error: Unable to fetch data from the API."

    return render_template('Weather.html',
        variable1=f" Temperature in {CITY}: {temp_fahrenheit:.2f}°F ",
        variable2=f" It feels like {feels_like_fahrenheit:.2f}°F in {CITY}: ",
        variable3=f" Humidity in {CITY}: {humidity}% ",
        variable4=f" Wind Speed in {CITY}: {wind_speed} MPH ",
        variable5=f" General Weather in {CITY}: {description} ",
        variable6=f" Sun rises in {CITY} at {sunrise_time} local time. ",
        variable7=f" Sun sets in {CITY} at {sunset_time} local time. "
    )



if __name__ == '__main__':
    app.run(debug=True)
