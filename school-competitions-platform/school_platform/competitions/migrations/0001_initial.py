# Generated by Django 4.2.6 on 2023-10-27 20:35

import ckeditor_uploader.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название конкурса')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='описание конкурса')),
                ('maximum_number_of_event_participants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='максимальное количество участников мероприятия')),
                ('maximum_number_of_team_members', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='максимальное количество участников в команде')),
                ('maximum_commands_per_class', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='максимальное количество команд от класса')),
                ('maximum_commands', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='максимальное количество команд')),
                ('only_for_current_school', models.BooleanField(blank=True, default=True, verbose_name='конкурс только для учащихся данного учебного заведения')),
                ('commands_only_from_classes', models.BooleanField(blank=True, default=True, verbose_name='команды только от классов')),
                ('is_competition_individual', models.BooleanField(blank=True, default=True, verbose_name='является ли конкурс индивидуальным')),
                ('status', models.CharField(blank=True, choices=[('registration_pending', 'Ожидание регистрации'), ('registration_open', 'Регистрация открыта'), ('ongoing', 'В процессе'), ('completed', 'Завершено'), ('cancelled', 'Отменено'), ('postponed', 'Отложено')], max_length=50, verbose_name='статус конкурса')),
                ('is_draft', models.BooleanField(blank=True, default=False, verbose_name='черновик')),
                ('date_of_ending_registration', models.DateField(verbose_name='дата окончания регистрации')),
                ('date_of_starting_registration', models.DateField(verbose_name='дата начала регистрации')),
                ('date_of_starting_competition', models.DateField(verbose_name='дата начала конкурса')),
            ],
            options={
                'verbose_name': 'конкурс',
                'verbose_name_plural': 'конкурсы',
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='competition', to='competitions.competition', verbose_name='конкурс')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participant', to=settings.AUTH_USER_MODEL, verbose_name='участник')),
            ],
            options={
                'verbose_name': 'участник',
                'verbose_name_plural': 'участники',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='название команды')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='competitions.competition', verbose_name='конкурс')),
                ('participants', models.ManyToManyField(blank=True, related_name='teams', to='competitions.participant', verbose_name='участники')),
                ('school_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='schools.class', verbose_name='класс')),
            ],
            options={
                'verbose_name': 'команда',
                'verbose_name_plural': 'команды',
            },
        ),
        migrations.AddField(
            model_name='competition',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='competitions', to='competitions.participant', verbose_name='участники'),
        ),
        migrations.AddField(
            model_name='competition',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='competitions', to='competitions.team', verbose_name='команды'),
        ),
    ]