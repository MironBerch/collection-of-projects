from django.shortcuts import render, redirect
from django.contrib import messages
from fast_auth.forms import SigninForm, CreateUserForm
from django.views import View
from django.contrib.auth import login, logout, authenticate


class SignupView(View):
    """Sign up view class"""
    def get(self, request):
        form = CreateUserForm()

        context = {
            'form': form,
        }

        return render(request, 'fast_auth/signup.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created ' + user)
            return redirect('signin')

        context = {
            'form': form,
        }
        return render(request, 'fast_auth/signup.html', context)
        

            
class SigninView(View):
    """Sign in view class"""
    def get(self, request):
        form = SigninForm()

        context = {
            'form': form,
        }

        return render(request, 'fast_auth/signin.html', context)

    def post(self, request):
        form = SigninForm(request.POST)

        context = {
            'form': form,
        }

        if form.is_valid():
            data_user = form.cleaned_data.get('user')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=data_user, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username or password is not correct')
                return render(request, 'fast_auth/signin.html', context)

        return render(request, 'fast_auth/signin.html', context)


class LogoutView(View):
    """Log out view class"""
    def get(self, request):
        return render(request, 'fast_auth/logout.html')

    def post(self, request):
        logout(request)
        return redirect('signin')