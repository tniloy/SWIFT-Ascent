'''
The OpenWeatherMap API provides weather data for a specific location by city name or geographical coordinates. This documentation will cover the endpoint https://api.openweathermap.org/data/2.5/weather.

Request
This endpoint accepts both GET and POST requests.

URL Parameters
The following parameters should be included in the URL to specify the location for which to retrieve weather data:

q (string): city name and country code separated by a comma (e.g. q=London,UK)
lat (float): latitude of the location
lon (float): longitude of the location
You need to include either q, or both lat and lon in the request URL.

Query Parameters
The following parameters can be included as query parameters in the URL to modify the request:

appid (string): your OpenWeatherMap API key. Required.
units (string): the units of measurement to use for temperature and other values. Options are metric (Celsius) and imperial (Fahrenheit). Default is metric.
lang (string): the language to return the response in. Options include en, de, fr, etc. Default is en.
Response
The response will be in JSON format and will include the following information:

coord (object): information about the location's geographical coordinates
lon (float): longitude
lat (float): latitude
weather (array): an array of objects describing the weather conditions
id (integer): a unique identifier for the weather condition
main (string): a brief description of the weather condition
description (string): a more detailed description of the weather condition
icon (string): a code representing the weather condition (used to display an appropriate weather icon)
base (string): the base station for the weather data
main (object): information about the current weather conditions
temp (float): the current temperature
pressure (float): the atmospheric pressure
humidity (integer): the humidity in percentage
temp_min (float): the minimum temperature
temp_max (float): the maximum temperature
visibility (integer): the visibility in meters
wind (object): information about the wind conditions
speed (float): the wind speed
deg (integer): the wind direction in degrees
clouds (object): information about cloud coverage
all (integer): the percentage of cloud coverage
dt (integer): the time of data calculation, unix, UTC
sys (object): information about the system that generated the data
type (integer): the internal system ID of the data source
id (integer): the internal system ID of the data source
message (float): the data request success rate
country (string): the country code of the location
sunrise (integer): the time of sunrise, unix, UTC
sunset (integer): the time of sunset, unix, UTC
id (integer): the location's unique OpenWeatherMap ID
name (string):

'''


import requests


def get_weather(location, api_key):
    if location.isdigit():
        # location is a set of coordinates
        lat, lon = map(float, location.split(','))
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    else:
        # location is a city name
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def main(api_key, location='New York'):
    weather_info = get_weather(location, api_key)
    if weather_info:
        # display some of the weather information
        print('Temperature:', weather_info['main']['temp'])
        print('Humidity:', weather_info['main']['humidity'])
        print('Weather:', weather_info['weather'][0]['description'])
    else:
        print('Could not retrieve weather information for', location)


if __name__ == '__main__':
    main('e7660ea6dbab337bee2f5b03497a496c', 'New York')