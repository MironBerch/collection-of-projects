from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic.base import TemplateResponseMixin

from user_authentication.forms import SigninForm, SignupForm


class SignupView(
    View,
    TemplateResponseMixin,
):
    """
    SignupView - view class for creating user object.
    """

    template_name = 'user_authentication/signup.html'
    form_class = SignupForm

    def get(self, request):
        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created ' + user)
            return redirect('signin')

        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )


class SigninView(
    View,
    TemplateResponseMixin,
):
    """
    SigninView - view class for user authentication.
    """

    template_name = 'user_authentication/signin.html'
    form_class = SigninForm

    def get(self, request):
        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )

    def post(self, request):
        form = SigninForm(request.POST)

        if form.is_valid():
            credentials = form.cleaned_data.get('credentials')
            password = form.cleaned_data.get('password')

            user = authenticate(request, credentials=credentials, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username or password is not correct')
                return self.render_to_response(
                    context={
                        'form': self.form_class(),
                    },
                )

        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )


class SignoutView(
    View,
    TemplateResponseMixin,
):
    """
    SignoutView - view class for user logout.
    """

    template_name = 'user_authentication/signout.html'

    def get(self, request):
        return self.render_to_response(context={})

    def post(self, request):
        logout(request)
        return redirect('signin')
