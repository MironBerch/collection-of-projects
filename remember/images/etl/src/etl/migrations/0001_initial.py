# Generated by Django 5.0.6 on 2024-06-09 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('type', models.CharField(choices=[('sqlite', 'Sqlite'), ('postgresql', 'Postgresql'), ('elasticsearch', 'Elasticsearch')], max_length=13, verbose_name='тип')),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='название')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('type', models.CharField(choices=[('int', 'Int'), ('str', 'Str'), ('float', 'Float'), ('date', 'Date'), ('datetime', 'Datetime'), ('UUID', 'Uuid')], max_length=8, verbose_name='тип данных')),
                ('default', models.CharField(blank=True, max_length=255, null=True, verbose_name='значение по умолчанию')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='etl.model', verbose_name='модель частью которой является колонка')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled')], default='active', max_length=8, verbose_name='task status')),
                ('time_interval', models.CharField(choices=[('1 minute', 'One Min'), ('10 minutes', 'Ten Minutes'), ('1 hour', 'One Hour'), ('1 day', 'One Day')], default='1 minute', max_length=10, verbose_name='интервал')),
                ('sync', models.BooleanField(default=False, verbose_name='синхронизировать данные')),
                ('from_table', models.CharField(max_length=255)),
                ('to_table', models.CharField(max_length=255)),
                ('index_column', models.CharField(default='id', max_length=255, verbose_name='первичный ключ')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etl.model', verbose_name='модель с которой связан процесс')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='etl.database', verbose_name='исходная бд')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='etl.database', verbose_name='целевая бд')),
                ('task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask')),
            ],
            options={
                'verbose_name_plural': 'Processes',
            },
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_name', models.CharField(max_length=50)),
                ('table', models.CharField(max_length=50, verbose_name='таблица')),
                ('through_table', models.CharField(max_length=50, verbose_name='промежуточная таблица')),
                ('suffix', models.CharField(default='_id', max_length=25)),
                ('flat', models.BooleanField(default=False, verbose_name='храниться ли связанные данные в одной таблице')),
                ('condition', models.CharField(blank=True, max_length=255, null=True, verbose_name='условие')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='etl.model', verbose_name='модель')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='etl.process', verbose_name='процесс')),
            ],
        ),
    ]
