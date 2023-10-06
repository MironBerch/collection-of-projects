from email.message import EmailMessage
from urllib.parse import urlencode

from config import settings


def get_user_verify_email_template(
        user_email: str,
        username: str,
        verify_email_link: str,
):
    email = EmailMessage()
    email['Subject'] = 'Account verify at Pastebin'
    email['From'] = settings.email_host_user
    email['To'] = user_email

    email.set_content(
        f'<div>'
        f'<h1>Hello {username},</h1>'
        f'<p>Follow the link below to verify your email:</p>'
        f'<a href="{verify_email_link}">{verify_email_link}</a>'
        f'</div>',
        subtype='html',
    )
    return email


def get_password_reset_template(
        user_email: str,
        password_reset_link: str,
        username: str,
):
    email = EmailMessage()
    email['Subject'] = 'Password reset at Pastebin'
    email['From'] = settings.email_host_user
    email['To'] = user_email

    email.set_content(
        f'<h1>Hello {username},</h1>'
        f'<p>You recently requested to reset your password for your '
        f'{settings.project_domain} account. Click the link below to reset '
        'it.</p>'
        f'<a href="{password_reset_link}">{password_reset_link}</a>'
        f'<p>If you did not request a password reset, please ignore '
        'this email.</p>'
        f'<br>'
        f'<p>Thanks,<br>{settings.project_domain} Team</p>',
        subtype='html',
    )
    return email


def create_verify_email_link(token: str) -> str:
    """Create the verification link for the user's email confirmation."""
    params = {'token': token}
    query_params = urlencode(params)
    return (
        f'{settings.project_full_domain}:8000/auth/verify-email?{query_params}'
    )


def create_reset_password_link(token: str) -> str:
    """Create the link for reset user's password."""
    params = {'token': token}
    query_params = urlencode(params)
    return (
        f'{settings.project_full_domain}'
        f':8000/auth/password-reset?{query_params}'
    )
