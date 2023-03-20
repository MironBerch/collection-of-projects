from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class SignupForm(UserCreationForm):
    """Form for creation new account."""

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class SigninForm(forms.Form):
    """Form for sign in account."""

    username = forms.CharField(
        widget=forms.TextInput(),
        max_length=60, 
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=30,
        required=True,
    )


class EmailConfirmForm(forms.Form):
    """Form for confirm user email"""

    code = forms.CharField(
        widget=forms.TextInput(),
        max_length=8,
    )