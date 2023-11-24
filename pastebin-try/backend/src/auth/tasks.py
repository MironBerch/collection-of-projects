import smtplib

from celery import shared_task

from auth.services import (
    get_password_reset_template,
    get_user_verify_email_template,
)
from config import settings


@shared_task()
def send_user_verify_email(
        user_email: str,
        username: str,
        verify_email_link: str,
) -> None:
    email = get_user_verify_email_template(
        user_email=user_email,
        username=username,
        verify_email_link=verify_email_link,
    )
    with smtplib.SMTP_SSL(settings.email_host, settings.email_port) as server:
        server.login(settings.email_host_user, settings.email_host_password)
        server.send_message(email)


@shared_task()
def send_password_reset_email(
        user_email: str,
        password_reset_link: str,
        username: str,
) -> None:
    email = get_password_reset_template(
        user_email=user_email,
        username=username,
        password_reset_link=password_reset_link,
    )
    with smtplib.SMTP_SSL(settings.email_host, settings.email_port) as server:
        server.login(settings.email_host_user, settings.email_host_password)
        server.send_message(email)
