from django.db import models

from accounts.models import User
from students.models import Student


def contest_diplom_scan_path(instance, filename):
    """Create path for diplom scans"""
    return 'diplom_scans/{0}/{1}/{2}'.format(
        instance.student.full_name,
        instance.title,
        instance.result,
    )


class Contest(models.Model):
    SUBJECT_CHOICES = (
        ('Русский язык', 'Русский язык'),
        ('Литературное чтение', 'Литературное чтение'),
        ('Математика', 'Математика'),
        ('Окружающий мир', 'Окружающий мир'),
        ('Музыка', 'Музыка'),
        ('ИЗО', 'ИЗО'),
        ('Технология', 'Технология'),
        ('Физическая культура', 'Физическая культура'),
        ('Английский язык', 'Английский язык'),
        ('ОРКСЭ', 'ОРКСЭ'),
        ('Литература', 'Литература'),
        ('История', 'История'),
        ('Обществознание', 'Обществознание'),
        ('География', 'География'),
        ('Биология', 'Биология'),
        ('ОБЖ', 'ОБЖ'),
        ('Экономика', 'Экономика'),
        ('Технология', 'Технология'),
        ('Химия', 'Химия'),
        ('Физика', 'Физика'),
        ('Информатика', 'Информатика'),
        ('Проектная деятельность', 'Проектная деятельность'),
    )
    STAGE_CHOICES = (
        ('Школьный', 'Школьный'),
        ('Районный', 'Районный'),
        ('Городской', 'Городской'),
        ('Региональный', 'Региональный'),
        ('Всероссийский', 'Всероссийский'),
        ('Международный', 'Международный'),
    )
    DIRECTION_CHOICES = (
        ('Спорт', 'Спорт'),
        ('Образование', 'Образование'),
        ('Исскуство', 'Исскуство'),
        ('Культура', 'Культура'),
        ('Социальное', 'Социальное'),
        ('Олимпиада', 'Олимпиада'),
    )
    RESULT_CHOICES = (
        ('1 место', '1 место'),
        ('2 место', '2 место'),
        ('3 место', '3 место'),
        ('Призёр', 'Призёр'),
        ('Победитель', 'Победитель'),
        ('Лауреат', 'Лауреат'),
        ('Участник', 'Участник'),
        ('Дипломат', 'Дипломат'),
    )
    contest_creater = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Создатель учёта мероприятия',
    )
    creation_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата учёта мероприятия',
    )
    modified_date = models.DateField(
        auto_now=True,
        verbose_name='Дата последнего изменения учёта',
    )
    event_date = models.DateField(
        editable=True,
        verbose_name='Дата проведения мероприятия',
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название мероприятия',
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Ученик учавствующий в мероприятии',
    )
    other = models.TextField(
        blank=True,
        null=True,
        verbose_name='Комментарии учителя',
    )
    teachers_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='ФИО ответсвенного руководителя',
    )
    stage = models.CharField(
        choices=STAGE_CHOICES,
        max_length=25,
        verbose_name='Этап мероприятия',
    )
    direction = models.CharField(
        choices=DIRECTION_CHOICES,
        max_length=25,
        verbose_name='Направление мероприятия',
    )
    subject = models.CharField(
        choices=SUBJECT_CHOICES,
        max_length=25,
        verbose_name='Предметная область мероприятия',
    )
    scan_diploma = models.FileField(
        upload_to=contest_diplom_scan_path,
        null=True,
        blank=True,
        verbose_name='Скан диплома',
    )
    result = models.CharField(
        choices=RESULT_CHOICES,
        max_length=25,
        verbose_name='Результат мероприятия',
    )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
