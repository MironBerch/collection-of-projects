from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from django.contrib import messages
from .services import weather_data_json_format


def main(request):
    """Main weather-app function"""
    API_KEY = '257d33e204cb72ae037cc13895272f13'
    URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + API_KEY

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form_processing(request, form, URL)

    form = CityForm()

    weather_objects = weather_data_json_format(URL)
    
    context = {
        'weather_data': weather_objects,
        'form': form,
    }
    
    return render(request, 'main.html', context)


def form_processing(request, form, URL):
    """Processing function save form or return error message"""
    add_city = form.cleaned_data['name']
    add_city_count = City.objects.filter(name=add_city).count()
    if add_city_count == 0:
        add_city_json = requests.get(URL.format(add_city)).json()
        if add_city_json['cod'] == 200:
            form.save()
        else:
            messages.info(request, 'City does not exists')
    else:
        messages.error(request, 'City exists in db')


def delete_city(request, city_name):
    City.objects.filter(name=city_name).delete()
    return redirect('main')