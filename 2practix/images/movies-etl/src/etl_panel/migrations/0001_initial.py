# Generated by Django 5.0.3 on 2024-04-07 20:51

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
                ('type', models.CharField(choices=[('sqlite', 'sqlite'), ('postgresql', 'postgresql'), ('elasticsearch', 'elasticsearch')], max_length=50)),
                ('uri', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('str', 'str'), ('int', 'int'), ('float', 'float'), ('date', 'date'), ('datetime', 'datetime'), ('UUID', 'UUID')], max_length=50)),
                ('default', models.CharField(blank=True, max_length=255)),
                ('alias', models.CharField(blank=True, max_length=255)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='etl_panel.model')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('disabled', 'disabled')], default='active', max_length=50)),
                ('from_table', models.CharField(max_length=255)),
                ('to_table', models.CharField(max_length=255)),
                ('index_column', models.CharField(default='id', max_length=255)),
                ('sync', models.BooleanField(default=False)),
                ('time_interval', models.CharField(choices=[('1 minute', '1 minute'), ('5 minutes', '5 minutes'), ('1 hour', '1 hour')], default='1 minute', max_length=50)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etl_panel.model')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='etl_panel.database')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='etl_panel.database')),
                ('task', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask')),
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
                ('table', models.CharField(max_length=50)),
                ('through_table', models.CharField(max_length=50)),
                ('suffix', models.CharField(default='_id', max_length=50)),
                ('flat', models.BooleanField(default=False)),
                ('condition', models.CharField(blank=True, max_length=255)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='etl_panel.model')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='etl_panel.process')),
            ],
        ),
    ]
