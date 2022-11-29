from .models import City
from django.forms import ModelForm
from django import forms


class CityForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
            'class': 'form-control form-control-lg',
            'type': 'text',
            'aria-label': '.form-control-lg example',
            'placeholder': 'Город'
            }
        )
    )

    class Meta:
        model = City
        fields = ('name',)