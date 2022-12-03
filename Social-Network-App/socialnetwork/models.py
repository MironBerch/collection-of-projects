from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length=1000)
    avatar = models.ImageField(upload_to='avatars')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=50)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user