from django.db import models


class Class(models.Model):
    school_class = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Школьный класс',
        primary_key=True,
    )

    def __str__(self):
        return self.school_class

    class Meta:
        verbose_name = 'Школьный класс'
        verbose_name_plural = 'Школьные классы'
