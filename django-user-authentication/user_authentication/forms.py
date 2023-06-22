from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    """
    Sign up form for user authentication.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password1',
            'password2',
        )


class SigninForm(forms.Form):
    """
    Sign in form for user authentication. \n
    credentials - char field for user authentication (email or username).
    """

    credentials = forms.CharField(
        max_length=255,
    )
    password = forms.CharField(
        max_length=255,
    )
