from django.db import models
from django.contrib.auth.models import AbstractUser

from shortuuidfield import ShortUUIDField


class User(AbstractUser):
    userId = ShortUUIDField()
    image = models.ImageField(
        upload_to='users/',
    )


class OnlineUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


class ChatRoom(models.Model):
    roomId = ShortUUIDField()
    type = models.CharField(
        max_length=10,
        default='DM',
    )
    member = models.ManyToManyField(User)
    name = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            self.roomId + ' -> ' + str(self.name)
        )


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        ChatRoom,
        on_delete=models.SET_NULL,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    message = models.CharField(
        max_length=255,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.message
