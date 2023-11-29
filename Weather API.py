import requests
from pprint import PrettyPrinter

API_KEY = 'a19a1a4743663d46ff15ac3298f3d3c2'
GEO_URL = 'http://api.openweathermap.org/geo/1.0/direct'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
LIMIT = '5'

printer = PrettyPrinter()

city = input('Enter the city name: ')

geo_request_url = f'{GEO_URL}?q={city}&limit={LIMIT}&appid={API_KEY}'
geo_response = requests.get(geo_request_url)

if geo_response.status_code == 200:
    lat = geo_response.json()[0]['lat']
    lon = geo_response.json()[0]['lon']
else:
    print(f'Error: {geo_response.status_code}')

weather_request_url = f'{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}'
weather_reponse = requests.get(weather_request_url)

if weather_reponse.status_code == 200:
    temperature = round(weather_reponse.json()['main']['temp'] - 273.15)
    weather = weather_reponse.json()['weather'][0]['description']
    
else:
    print(f'Error: {weather_reponse.status_code}')

print(f'The weather in {city} is: ')
print(f'Temperature: {temperature} \u00B0C')
print(f'Weather: {weather}')