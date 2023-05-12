from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.mixins import AnonymousUserRequiredMixin
from accounts.forms import SignupForm, SigninForm
from accounts.models import User


class SignupView(
    AnonymousUserRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for creating new user"""

    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get(self, request):
        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )

    def post(self, request):
        form = SignupForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            patronymic = form.cleaned_data.get('patronymic')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                email=email,
                name=name,
                surname=surname,
                patronymic=patronymic,
                password=password,
            )
            messages.success(
                request,
                'Пользователь зарегистрирован. Подождите активации пользователя администратором.'
            )
            return redirect('signin')

        messages.success(request, 'Пароли не совпадают.')

        return self.render_to_response(
            context={
                'form': form,
            },
        )


class SigninView(
    AnonymousUserRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """View for login in system"""

    template_name = 'registration/signin.html'
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
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('list')

            messages.warning(request, 'Неправильная почта или пароль.')

        return self.render_to_response(
            context={
                'form': form,
            },
        )


class SignoutView(
    LoginRequiredMixin,
    View,
):
    """View for sign out from system"""

    def get(self, request):
        return render(request, 'registration/signout.html')

    def post(self, request):
        logout(request)
        return redirect('signin')
