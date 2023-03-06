from random import randint

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from accounts.models import  EmailConfirmMessage, User


def get_user_by_username(username):
    """Get user by username"""
    user = get_object_or_404(User, username=username)
    return user


def generate_random_email_confirm_code() -> str:
    """Generates random 8 digits code (00000000-99999999)."""
    return str(randint(0, 99999999)).zfill(8)


def create_email_confirmation_model(request):
    """Create email confirmation model"""
    if EmailConfirmMessage.objects.filter(email=request.user.email).exists():
        EmailConfirmMessage.objects.filter(email=request.user.email).delete()

    message = EmailConfirmMessage.objects.create(
        code=generate_random_email_confirm_code(), email=request.user.email
    )
    return message


def send_email_confirmation(email, confirmation_code) -> None:
    """Send confirmation email"""
    send_mail(
        subject='Verify email',
        message=f'Hello. Code: {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


def get_user_email_confirmation_message(request):
    """Get user email confirmation message"""
    message = get_object_or_404(EmailConfirmMessage, email=request.user.email)
    return message