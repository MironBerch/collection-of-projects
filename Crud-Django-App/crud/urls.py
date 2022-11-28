from django.urls import path
from .views import note_list, note_detail, note_create, note_delete


urlpatterns = [
    path('', note_list, name='list'),
    path('<int:pk>/', note_detail, name='detail'),
    path('create/', note_create, name='create'),
    path('delete/<int:pk>', note_delete, name='delete'),
]