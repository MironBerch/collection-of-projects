from django.db import models

from accounts.models import User
from people.models import Person
from characters.models import Character


class Staff(models.Model):
    """Anime creators"""
    ROLE_CHOICES = (
        ('original author', 'Автор оригинала'),
        ('producer', 'Режиссёр'),
        ('art director', 'Арт-директор'),
        ('producer assistant', 'Ассистент продюсера'),
        ('chief animator', 'Главный аниматор'),
        ('sound engineer', 'Звукорежиссёр'),
        ('execution ch. music topics', 'Исполнение гл. муз. темы'),
        ('scenario', 'Сценарий'),
        ('animation director', 'Режиссёр анимации'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name='person',
    )


def get_studio_image_upload_path(instance: 'Studio', filename: str) -> str:
    return f'upload/studio/{instance.name}/{filename}'


class Studio(models.Model):
    """Anime studio"""
    name = models.CharField(max_length=50)
    studio_image = models.ImageField(
        upload_to=get_studio_image_upload_path,
        blank=True,
        null=True,
    )


class Genre(models.Model):
    """Anime genre"""
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    url = models.SlugField(max_length=40, unique=True)


def get_studio_image_upload_path(instance: 'Anime', filename: str) -> str:
    return f'upload/anime/{instance.name}/{filename}'


class Anime(models.Model):
    ANIME_TYPE = (
        ('tv series', 'ТВ сериал'),
        ('film', 'Фильм'),
        ('OVA', 'OVA'),
        ('ONA', 'ONA'),
        ('special', 'Спешл'),
    )
    ANIME_STATUS = (
        ('announced', 'Анонсировано'),
        ('ongoing', 'Онгоинг'),
        ('released', 'Вышедшее'),
    )
    name = models.CharField(max_length=100)
    poster = models.ImageField(
        upload_to=get_studio_image_upload_path,
    )
    episodes = models.IntegerField(default=1)
    episode_duration = models.CharField(max_length=20)
    anime_type = models.CharField(max_length=10, choices=ANIME_TYPE)
    anime_status = models.CharField(max_length=10, choices=ANIME_STATUS)
    genres = models.ManyToManyField(Genre)
    alternative_name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    studio = models.ManyToManyField(Studio)
    staff = models.ManyToManyField(Staff)
    characters = models.ManyToManyField(Character)
    trailer = models.URLField(max_length=100)


class AnimeReview(models.Model):
    """Anime review"""
    OPINION_CHOICES = (
        ('positive', 'Положительный'),
        ('neutral', 'Нейтральный'),
        ('negative', 'Отрицательный'),
    ) 
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        verbose_name='anime',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='review author',
    )
    content = models.TextField()
    opinion = models.CharField(
        choices=OPINION_CHOICES,
        max_length=15,
        verbose_name='reviewer opinion about anime',
    )


class AnimeComment(models.Model):
    """Anime comment"""
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        verbose_name='anime',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='review author',
    )
    content = models.TextField()


def get_anime_shots_image_upload_path(instance: 'AnimeShots', filename: str) -> str:
    return f'upload/anime_shots/{instance.anime}/{filename}'


class AnimeShots(models.Model):
    """Anime shots"""
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        verbose_name='anime',
    )
    image = models.ImageField(upload_to=get_anime_shots_image_upload_path)