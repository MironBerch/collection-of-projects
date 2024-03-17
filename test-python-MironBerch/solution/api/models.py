import datetime

from django.db import models
import uuid
from users.models import User


class Country(models.Model):
    name = models.CharField(max_length=255)
    alpha2 = models.TextField(max_length=255)
    alpha3 = models.TextField(max_length=255)
    region = models.TextField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'custom_country_table_name'


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dislikesCount = models.PositiveIntegerField(default=0)
    likesCount = models.PositiveIntegerField(default=0)
    addedAt = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.addedAt:
            self.addedAt = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        super(Post, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
