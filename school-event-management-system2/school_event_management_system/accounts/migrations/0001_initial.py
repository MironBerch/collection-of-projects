# Generated by Django 4.2.7 on 2023-11-03 00:43

import accounts.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='почта')),
                ('name', models.CharField(max_length=30, verbose_name='имя')),
                ('surname', models.CharField(max_length=30, verbose_name='фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=30, verbose_name='отчество')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='дата присоединения')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='последний вход в систему')),
                ('role', models.CharField(choices=[('ученик', 'ученик'), ('учитель', 'учитель')], default='ученик', max_length=10, verbose_name='роль')),
                ('is_email_confirmed', models.BooleanField(default=False, verbose_name='электронная почта подтверждена')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='персонал')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='суперпользователь')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
                ('activated', accounts.managers.ActivatedAccountsManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='дата рождения')),
            ],
            options={
                'verbose_name': 'профиль',
                'verbose_name_plural': 'профили',
            },
        ),
    ]