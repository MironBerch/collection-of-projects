from django.urls import path
from .views import main, delete_city


urlpatterns = [
    path('', main, name='main'),
    path('delete/<city_name>/', delete_city, name='delete_city')
]