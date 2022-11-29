import requests
from .models import City
from typing import List


def weather_data_json_format(URL) -> List:
    """Return weather objects from db"""
    cities = City.objects.all()
    weather_objects = []

    for city in cities:
        request = requests.get(URL.format(city)).json()
        city_info = {
            'city': city.name,
            'temp': request['main']['temp'],
            'icon': request['weather'][0]['icon'],
        }
        weather_objects.append(city_info)

    return weather_objects 