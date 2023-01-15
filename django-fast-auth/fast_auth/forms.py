from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SigninForm(forms.Form):
    user = forms.CharField(
        label='Email or username', widget=forms.TextInput(), max_length=50, required=True
    )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(), max_length=50, required=True
    )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')