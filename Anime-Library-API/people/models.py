from django.db import models

from accounts.models import User


def get_person_image_upload_path(instance: 'Person', filename: str) -> str:
    return f'upload/person/{instance.full_name}/{filename}'


def get_default_person_image() -> str:
    return f'default/default_person_image.png'


class Person(models.Model):
    ACTIVITY_CHOICES = (
        ('seiyu', 'Сэйю'),
        ('producer', 'Режиссёр'),
        ('mangakas', 'Мангака'),
        ('anime creator', 'Создатель аниме')
    )
    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=get_person_image_upload_path,
        default=get_default_person_image,
    )
    description = models.TextField(max_length=3000)


class PersonComment(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name='person comment',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='comment author',
    )
    content = models.TextField(
        max_length=1000,
        verbose_name='comment content',
    )
    date = models.DateField(auto_now_add=True)