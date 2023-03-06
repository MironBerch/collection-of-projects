from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView,  PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView

from accounts.services import send_email_confirmation, create_email_confirmation_model, get_user_email_confirmation_message
from accounts.forms import SignupForm, SigninForm, EmailConfirmForm
from accounts.mixins import AnonymousUserRequiredMixin, EmailNotConfirmedUserRequiredMixin
from profiles.services import create_profile


class SignupView(
    AnonymousUserRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """Sign-up view class."""

    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        return self.render_to_response(
            context = {
                'form': self.form_class(),
            },
        )

    def post(self, request):
        form = SignupForm(request.POST or None)

        if form.is_valid():
            user = form.save()
            create_profile(user=user)
            return redirect('signin')

        return self.render_to_response(
            context={
                'form': form,
            },
        )


class EmailConfirmationView(
    LoginRequiredMixin,
    EmailNotConfirmedUserRequiredMixin,
    TemplateResponseMixin,
    View,
):
    """Email Confirmation view class."""

    form_class = EmailConfirmForm
    template_name = 'accounts/email_confirm.html'

    def get(self, request):
        message = create_email_confirmation_model(request)
        send_email_confirmation(
            email=request.user.email, confirmation_code=message.code,
        )
        
        return self.render_to_response(
            context={
                'form': self.form_class(),
            },
        )

    def post(self, request):
        message = get_user_email_confirmation_message(request)
        form = EmailConfirmForm(request.POST or None)
        user = request.user

        if form.is_valid():
            code = form.cleaned_data.get('code')
            if message.code == code:
                user.is_email_confirmed = True
                user.save()
                return redirect('signin')
            
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
    """Sign-in view class."""

    form_class = SigninForm
    template_name = 'accounts/signin.html'

    def get(self, request):
        return self.render_to_response(
            context = {
                'form': self.form_class(),
            },
        )

    def post(self, request):
        form = SigninForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('signout')

            messages.warning(request, 'Username or password not correct.')

        return self.render_to_response(
            context={
                'form': form,
            },
        )


class SignoutView(
    LoginRequiredMixin,
    View,
):
    """Sign-out view class."""

    def get(self, request):
        return render(request, 'accounts/signout.html')

    def post(self, request):
        logout(request)
        return redirect('signin')
    

class PasswordResetView(PasswordResetView):
    """Password reset view."""

    template_name = 'accounts/password_reset.html'


class PasswordResetDoneView(PasswordResetDoneView):
    """Password reset done view."""

    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    """Password reset confirm view."""

    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset complete view."""

    template_name = 'accounts/password_reset_complete.html'


class PasswordChangeView(PasswordChangeView):
    """Pasword change view"""

    template_name = 'accounts/password_change.html'


class PasswordChangeDoneView(PasswordChangeDoneView):
    """Pasword change done view"""

    template_name = 'accounts/password_change_done.html'