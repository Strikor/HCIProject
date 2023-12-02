from flask import Flask, Response, render_template
import datetime as dt
import requests

app = Flask(__name__)

def kelvin_to_fahrenhite(kelvin):
    celsius = kelvin - 273.15
    fahrenhite = celsius * (9/5) + 32
    return fahrenhite
        
def mps_to_mph(mps):
    mph = (mps * 2.237)
    return mph

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "6af6a8ccf981a5901934b56fc6850cf7"
CITY = "Kent, US, 67"
url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()


#Tempture
temp_kelvin = response['main']['temp']
temp_fahrenhite = kelvin_to_fahrenhite(temp_kelvin)
#Feels like
feels_like_kelvin = response['main']['feels_like']
feels_like_fahrenhite = kelvin_to_fahrenhite(feels_like_kelvin)
#Humidity
humidity = response['main']['humidity']
#Weather description
description = response['weather'][0]['description']
#Sunrise Time
sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
#Sunset Time
sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
#Wind Speed
wind_speed_in_mps = response['wind']['speed']
wind_speed = mps_to_mph(wind_speed_in_mps)


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


@app.route('/Weather.html')
def Weather():
    return render_template('Weather.html',
        variable1 = (f" Tempture in Kent: {temp_fahrenhite:.2f}°F "),
        variable2 = (f" It feels like {feels_like_fahrenhite:.2f}°F in Kent: "),
        variable3 = (f" Humidity in Kent: {humidity}% "),
        variable4 = (f" Wind Speed in Kent: {wind_speed}MPH "),
        variable5 = (f" General Weather in Kent: {description} "),
        variable6 = (f" Sun rises in Kent at {sunrise_time} local time. "),
        variable7 = (f" Sun sets in Kent at {sunset_time} local time. "))


if __name__ == 'main':
    app.run(debug=True)
