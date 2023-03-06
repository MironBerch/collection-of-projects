from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from accounts.models import User
from notifications.models import Notification


def get_profile_image_upload_path(instance: 'Profile', filename: str) -> str:
    return f'upload/users/{instance.user.email}/profile/{filename}'


def get_default_profile_image() -> str:
    return f'default/default_profile_image.png'


class Profile(models.Model):
    """Profile model for User"""

    GENDER_CHOICES = (
        ('Man', 'Man'),
        ('Woman', 'Woman'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
    )
    profile_image = models.ImageField(
        verbose_name='profile image',
        blank=True,
        null=True,
        upload_to=get_profile_image_upload_path,
        default=get_default_profile_image,
    )
    birthday = models.DateField(
        verbose_name='birthday',
        blank=True,
        null=True,
    )
    gender = models.CharField(
        verbose_name='gender',
        choices=GENDER_CHOICES,
        max_length=5,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='description',
        max_length=1000,
        blank=True,
        null=True,
    )


class ProfileComment(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='profile comment',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='comment author',
    )
    content = models.TextField(
        max_length=1000,
        verbose_name='comment content'
    )
    date = models.DateField(auto_now_add=True)

    def profile_comment(sender, instance, *args, **kwargs):
        comment = instance
        notify = Notification(user=comment.profile.user, sender=comment.author, content=comment.content)
        notify.save()


post_save.connect(ProfileComment.profile_comment, sender=ProfileComment)