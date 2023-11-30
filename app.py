from flask import Flask, render_template
import datetime as dt
import requests

app = Flask(__name__)

@app.route('/')

def api_main():
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "6af6a8ccf981a5901934b56fc6850cf7"
    CITY = "Kent"
    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()


if response.status_code == 200:
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
else:
        return "Error: Unable to fetch data from the API."

def kelvin_to_fahrenhite(kelvin):
    celsius = kelvin - 273.15
    fahrenhite = celsius * (9/5) + 32
    return fahrenhite
    
def mps_to_mph(mps):
    mph = (mps * 2.237)
    return mph

def template_render():
    return render_template('Weather.html',
        variable1 = (f" Tempture in {CITY}: {temp_fahrenhite:.2f}°F "),
        variable2 = (f" It feels like {feels_like_fahrenhite:.2f}°F in {CITY}: "),
        variable3 = (f" Humidity in {CITY}: {humidity}% "),
        variable4 = (f" Wind Speed in {CITY}: {wind_speed}MPH "),
        variable5 = (f" General Weather in {CITY}: {description} "),
        variable6 = (f" Sun rises in {CITY} at {sunrise_time} local time. "),
        variable7 = (f" Sun sets in {CITY} at {sunset_time} local time. "))
    
if __name__ == 'main':
    app.run(debug=True)
    
    