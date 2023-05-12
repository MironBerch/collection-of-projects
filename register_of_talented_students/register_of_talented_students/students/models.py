from django.db import models

from school_classes.models import Class


class StudentsBase(models.Model):
    """Students excel table"""
    file = models.FileField(
        upload_to='students/',
    )

    class Meta:
        verbose_name = 'Список учащихся'
        verbose_name_plural = "Списки учащихся"


class Student(models.Model):
    full_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='ФИО ученика',
    )
    school_class = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        verbose_name='Школьный класс',
    )
    is_learns = models.BooleanField(
        default=True,
        verbose_name='Проходит обучение',
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
