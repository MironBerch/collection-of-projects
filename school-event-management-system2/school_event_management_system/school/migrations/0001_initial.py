# Generated by Django 4.2.7 on 2023-11-03 00:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('school_class', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='класс')),
                ('year_of_study', models.SmallIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(11)])),
                ('class_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'класс',
                'verbose_name_plural': 'классы',
            },
        ),
    ]
