from ckeditor_uploader.fields import RichTextUploadingField

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


def get_event_image_upload_path(instance: 'Event', filename: str) -> str:
    return f'upload/{instance.name}/{filename}'


class ResultChoices(models.TextChoices):
    FIRST_PLACE = '1 место', '1 место'
    SECOND_PLACE = '2 место', '2 место'
    THIRD_PLACE = '3 место', '3 место'
    PRIZE_WINNER = 'Призёр', 'Призёр'
    WINNER = 'Победитель', 'Победитель'
    LAUREATE = 'Лауреат', 'Лауреат'
    PARTICIPANT = 'Участник', 'Участник'
    DIPLOMAT = 'Дипломат', 'Дипломат'


class EventStatusChoices(models.TextChoices):
    REGISTRATION_PENDING = 'Ожидание регистрации', 'Ожидание регистрации'
    REGISTRATION_OPEN = 'Регистрация открыта', 'Регистрация открыта'
    ONGOING = 'В процессе', 'В процессе'
    COMPLETED = 'Завершено', 'Завершено'
    CANCELLED = 'Отменено', 'Отменено'
    POSTPONED = 'Отложено', 'Отложено'


class EventTypeChoices(models.TextChoices):
    INDIVIDUAL = 'Индивидуальное', 'Индивидуальное'
    TEAM = 'Командное', 'Командное'
    CLASS_TEAMS = 'Командное от классов', 'Командное от классов'


class Event(models.Model):
    image = models.ImageField(
        verbose_name=_('изображение предварительного просмотра мероприятия'),
        blank=True,
        null=True,
        upload_to=get_event_image_upload_path,
    )
    name = models.CharField(
        verbose_name=_('название мероприятия'),
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_('url мероприятия'),
        max_length=100,
        unique=True,
    )
    description = RichTextUploadingField(
        verbose_name=_('описание мероприятия'),
        blank=True,
        null=True,
    )

    maximum_number_of_event_participants = models.IntegerField(
        verbose_name=_('максимальное количество участников мероприятия'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000),
        ],
    )
    maximum_commands = models.IntegerField(
        verbose_name=_('максимальное количество команд'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
    )
    maximum_commands_per_class = models.IntegerField(
        verbose_name=_('максимальное количество команд от класса'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        blank=True,
        null=True,
    )
    maximum_number_of_team_members = models.IntegerField(
        verbose_name=_('максимальное количество участников в команде'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
    )
    minimum_number_of_team_members = models.IntegerField(
        verbose_name=_('минимальное количество участников в команде'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name=_('статус мероприятия'),
        blank=True,
        max_length=50,
        choices=EventStatusChoices.choices,
    )
    type = models.CharField(
        verbose_name=_('тип мероприятия'),
        blank=True,
        max_length=50,
        choices=EventTypeChoices.choices,
    )

    date_of_ending_registration = models.DateField(
        verbose_name=_('дата окончания регистрации'),
    )
    date_of_starting_registration = models.DateField(
        verbose_name=_('дата начала регистрации'),
    )
    date_of_starting_event = models.DateField(
        verbose_name=_('дата начала мероприятия'),
    )

    published = models.BooleanField(
        verbose_name=_('опубликованные'),
        blank=True,
        default=False,
    )

    class Meta:
        verbose_name = _('мероприятие')
        verbose_name_plural = _('мероприятия')

    def __str__(self):
        return self.name


class Participant(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name=_('мероприятие'),
        on_delete=models.CASCADE,
        related_name='participants',
    )
    user = models.OneToOneField(
        User,
        verbose_name=_('пользователь'),
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        'Team',
        verbose_name=_('команда'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='participants',
    )

    class Meta:
        verbose_name = _('участник')
        verbose_name_plural = _('участники')

    def __str__(self):
        return f'{self.user} {self.event}'


class Team(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name=_('мероприятие'),
        on_delete=models.CASCADE,
        related_name='teams',
    )
    name = models.CharField(
        verbose_name=_('название команды'),
        max_length=100,
    )

    class Meta:
        verbose_name = _('команда')
        verbose_name_plural = _('команды')

    def __str__(self):
        return f'{self.name}'


def event_diplom_path(instance, filename):
    """Create path for diplom scans."""
    return 'diploms/{0}/{1}'.format(
        instance.event,
        filename,
    )


class Award(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name=_('мероприятие'),
        on_delete=models.CASCADE,
        related_name='awards',
    )
    participant = models.ForeignKey(
        Participant,
        verbose_name=_('участник'),
        on_delete=models.CASCADE,
        related_name='awards',
    )
    diplom = models.FileField(
        upload_to=event_diplom_path,
        null=True,
        blank=True,
        verbose_name=_('диплом'),
    )

    class Meta:
        verbose_name = _('диплом')
        verbose_name_plural = _('дипломы')

    def __str__(self):
        return f'{self.participant}'


class Result(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name=_('мероприятие'),
        on_delete=models.CASCADE,
        related_name='results',
    )
    participant = models.ForeignKey(
        Participant,
        verbose_name=_('участник'),
        on_delete=models.CASCADE,
        related_name='results',
        blank=True,
        null=True,
    )
    team = models.ForeignKey(
        Team,
        verbose_name=_('команда'),
        on_delete=models.CASCADE,
        related_name='results',
        blank=True,
        null=True,
    )
    result = models.CharField(
        verbose_name=_('место'),
        max_length=20,
        choices=ResultChoices.choices,
        default=ResultChoices.PARTICIPANT,
        blank=True,
    )

    class Meta:
        verbose_name = _('результат')
        verbose_name_plural = _('результаты')

    def __str__(self):
        if self.participant:
            return f'Результат для участника {self.participant.user}'
        if self.team:
            return f'Результат для команды {self.team.name}'
        return 'Результат'


class RegistrationForEventField(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name=_('мероприятие'),
    )
    label = models.CharField(
        max_length=100,
        verbose_name=_('ярлык'),
    )
    field_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('integer', 'Integer'),
            ('file', 'File'),
            ('float', 'Float'),
            ('char', 'Char'),
        ],
        default='text',
        verbose_name=_('тип поля'),
    )
    is_blank = models.BooleanField(
        default=True,
        verbose_name=_('является ли поле обязательным'),
    )

    class Meta:
        verbose_name = _('поле для формы регистрации на мероприятие')
        verbose_name_plural = _('поля для формы регистрации на мероприятие')

    def __str__(self):
        return f'{self.event} {self.label}'

    def create_form_field(self):
        if self.field_type == 'text':
            return forms.CharField(required=not self.is_blank)
        elif self.field_type == 'integer':
            return forms.IntegerField(required=not self.is_blank)
        elif self.field_type == 'file':
            return forms.FileField(required=not self.is_blank)
        elif self.field_type == 'float':
            return forms.FloatField(required=not self.is_blank)
        elif self.field_type == 'char':
            return forms.CharField(required=not self.is_blank)
        else:
            return None
