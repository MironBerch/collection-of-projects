from django.db import models

from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_recipient',
        verbose_name='notification recipient',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_sender',
        verbose_name='notification sender',
    )
    content = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='notification content',
    )
    is_seen = models.BooleanField(default=False)