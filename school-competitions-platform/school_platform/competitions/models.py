from ckeditor_uploader.fields import RichTextUploadingField

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from schools.models import Class


class StatusChoices(models.TextChoices):
    REGISTRATION_PENDING = 'registration_pending', 'Ожидание регистрации'
    REGISTRATION_OPEN = 'registration_open', 'Регистрация открыта'
    ONGOING = 'ongoing', 'В процессе'
    COMPLETED = 'completed', 'Завершено'
    CANCELLED = 'cancelled', 'Отменено'
    POSTPONED = 'postponed', 'Отложено'


class ResultChoices(models.TextChoices):
    FIRST_PLACE = '1 место', '1 место'
    SECOND_PLACE = '2 место', '2 место'
    THIRD_PLACE = '3 место', '3 место'
    PRIZE_WINNER = 'Призёр', 'Призёр'
    WINNER = 'Победитель', 'Победитель'
    LAUREATE = 'Лауреат', 'Лауреат'
    PARTICIPANT = 'Участник', 'Участник'
    DIPLOMAT = 'Дипломат', 'Дипломат'


def get_competition_image_upload_path(instance: 'Competition', filename: str) -> str:
    return f'upload/{instance.name}/{filename}'


class Competition(models.Model):
    image = models.ImageField(
        verbose_name=_('изображение'),
        blank=True,
        null=True,
        upload_to=get_competition_image_upload_path,
    )

    name = models.CharField(
        verbose_name=_('название конкурса'),
        max_length=100,
    )

    description = RichTextUploadingField(
        verbose_name=_('описание конкурса'),
        blank=True,
        null=True,
    )

    maximum_number_of_event_participants = models.IntegerField(
        verbose_name=_('максимальное количество участников мероприятия'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )

    maximum_number_of_team_members = models.IntegerField(
        verbose_name=_('максимальное количество участников в команде'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
    )

    maximum_commands_per_class = models.IntegerField(
        verbose_name=_('максимальное количество команд от класса'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        blank=True,
        null=True,
    )

    maximum_commands = models.IntegerField(
        verbose_name=_('максимальное количество команд'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
    )

    only_for_current_school = models.BooleanField(
        verbose_name=_('конкурс только для учащихся данного учебного заведения'),
        blank=True,
        default=True,
    )

    commands_only_from_classes = models.BooleanField(
        verbose_name=_('команды только от классов'),
        blank=True,
        default=True,
    )

    is_competition_individual = models.BooleanField(
        verbose_name=_('является ли конкурс индивидуальным'),
        blank=True,
        default=True,
    )

    status = models.CharField(
        verbose_name=_('статус конкурса'),
        blank=True,
        max_length=50,
        choices=StatusChoices.choices,
    )

    is_draft = models.BooleanField(
        verbose_name=_('черновик'),
        blank=True,
        default=False,
    )

    date_of_ending_registration = models.DateField(
        verbose_name=_('дата окончания регистрации'),
    )

    date_of_starting_registration = models.DateField(
        verbose_name=_('дата начала регистрации'),
    )

    date_of_starting_competition = models.DateField(
        verbose_name=_('дата начала конкурса'),
    )

    participants = models.ManyToManyField(
        'competitions.Participant',
        verbose_name=_('участники'),
        related_name='competitions',
        blank=True,
    )

    teams = models.ManyToManyField(
        'competitions.Team',
        verbose_name=_('команды'),
        related_name='competitions',
        blank=True,
    )

    class Meta:
        verbose_name = _('конкурс')
        verbose_name_plural = _('конкурсы')

    def __str__(self):
        return self.name


class Participant(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        related_name='competition',
        verbose_name=_('конкурс'),
    )
    result = models.CharField(
        max_length=100,
        choices=ResultChoices.choices,
        default=ResultChoices.PARTICIPANT,
        blank=True,
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='participant',
        verbose_name=_('участник'),
    )

    class Meta:
        verbose_name = _('участник')
        verbose_name_plural = _('участники')

    def __str__(self):
        return self.participant.full_name


class Team(models.Model):
    name = models.CharField(
        verbose_name=_('название команды'),
        max_length=50,
        blank=True,
    )
    participants = models.ManyToManyField(
        Participant,
        verbose_name=_('участники'),
        related_name='teams',
        blank=True,
    )
    school_class = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        verbose_name=_('класс'),
        null=True,
        blank=True,
    )
    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        verbose_name=_('конкурс'),
    )
    result = models.CharField(
        max_length=100,
        choices=ResultChoices.choices,
        default=ResultChoices.PARTICIPANT,
        blank=True,
    )

    class Meta:
        verbose_name = _('команда')
        verbose_name_plural = _('команды')

    def __str__(self):
        return self.name


def competition_diplom_path(instance, filename):
    """Create path for diplom scans"""
    return 'diploms/{0}/{1}'.format(
        instance.competition,
        filename,
    )


class Reward(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.PROTECT,
        verbose_name=_('участник'),
    )
    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        verbose_name=_('конкурс'),
    )
    result = models.CharField(
        max_length=100,
        choices=ResultChoices.choices,
        default=ResultChoices.PARTICIPANT,
        blank=True,
    )
    diplom = models.FileField(
        upload_to=competition_diplom_path,
        null=True,
        blank=True,
        verbose_name=_('диплом'),
    )

    class Meta:
        verbose_name = _('награда')
        verbose_name_plural = _('награды')

    def __str__(self):
        return self.participant.participant.full_name


class RegistrationForCompetitionField(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        verbose_name=_('конкурс'),
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
        verbose_name = _('поле для формы регистрации на конкурс')
        verbose_name_plural = _('поля для формы регистрации на конкурс')

    def __str__(self):
        return f'{self.competition} {self.label}'

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
