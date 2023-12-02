from flask import Flask, Response, render_template
import datetime as dt
import requests

app = Flask(__name__)

def kelvin_to_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return fahrenheit

def mps_to_mph(mps):
    mph = mps * 2.237
    return mph

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

@app.route('/StudentPlanner.html')
def StudentPlanner():
    return render_template('StudentPlanner.html')

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

@app.route('/Weather.html')
def Weather():
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "759cb2753beefcf28c82cafe746183ab"  # Replace with your actual API key
    CITY = "Kent"
    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()

    if response['cod'] == 200:  # Check for 'cod' instead of 'status_code'
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
