# Generated by Django 3.2.16 on 2024-09-04 14:05

import uuid

import django.core.validators
import django.db.models.deletion
import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventGuests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='EventImgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='events')),
            ],
        ),
        migrations.CreateModel(
            name='EventReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventReportTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('event_status', models.CharField(choices=[('not_started', 'Не почато'), ('in_process', 'Проходить'), ('ended', 'Завершилось')], db_index=True, default='not_started', max_length=32, verbose_name='Статус події')),
                ('event_age', models.CharField(choices=[('+0', '+0'), ('+6', '+6'), ('+12', '+12'), ('+16', '+16'), ('+18', '+18')], db_index=True, default='+0', max_length=4, verbose_name='Вікові обмеження')),
                ('begin_day', models.DateField(verbose_name='День проведення')),
                ('begin_time', models.TimeField(verbose_name='Час початку проведення події')),
                ('end_time', models.TimeField(verbose_name='Час кінця проведення події')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Назва події')),
                ('address', models.CharField(max_length=256, verbose_name='Адреса проведення')),
                ('description', models.CharField(max_length=512, verbose_name='Опис події')),
                ('main_photo', models.ImageField(upload_to='events/created/', verbose_name='Зображення заставки')),
                ('coordinates', models.JSONField(verbose_name='Координати')),
                ('price', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Ціна за вхід')),
                ('created_by_org', models.BooleanField(default=False, verbose_name='Створено організацією?')),
                ('result_revue', models.CharField(choices=[('approved', 'Підтверджено'), ('rejected', 'Відмова'), ('in_revue', 'На перевірці')], db_index=True, default='in_revue', max_length=64, verbose_name='Статус перевірки')),
                ('feedback', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Відгук модератора')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Подію створено')),
                ('last_time_updated', models.DateTimeField(blank=True, null=True, verbose_name='Подію редаговано')),
                ('is_repeatable', models.BooleanField(default=True, verbose_name='Дозволити пройти модерацію ще раз?')),
            ],
        ),
        migrations.CreateModel(
            name='EventStatusEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64, verbose_name='Статус події')),
                ('feedback', models.CharField(default='', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEvents',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('event_status', models.CharField(choices=[('not_started', 'Не почато'), ('in_process', 'Проходить'), ('ended', 'Завершилось')], db_index=True, default='not_started', max_length=32, verbose_name='Статус події')),
                ('event_age', models.CharField(choices=[('+0', '+0'), ('+6', '+6'), ('+12', '+12'), ('+16', '+16'), ('+18', '+18')], db_index=True, default='+0', max_length=4, verbose_name='Вікові обмеження')),
                ('begin_day', models.DateField(verbose_name='День проведення')),
                ('begin_time', models.TimeField(verbose_name='Час початку проведення події')),
                ('end_time', models.TimeField(verbose_name='Час кінця проведення події')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Назва події')),
                ('address', models.CharField(max_length=256, verbose_name='Адреса проведення')),
                ('description', models.CharField(max_length=512, verbose_name='Опис події')),
                ('main_photo', models.TextField(max_length=100, verbose_name='Зображення заставки')),
                ('coordinates', models.JSONField(verbose_name='Координати')),
                ('price', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Ціна за вхід')),
                ('created_by_org', models.BooleanField(default=False, verbose_name='Створено організацією?')),
                ('result_revue', models.CharField(choices=[('approved', 'Підтверджено'), ('rejected', 'Відмова'), ('in_revue', 'На перевірці')], db_index=True, default='in_revue', max_length=64, verbose_name='Статус перевірки')),
                ('feedback', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Відгук модератора')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Подію створено')),
                ('last_time_updated', models.DateTimeField(blank=True, null=True, verbose_name='Подію редаговано')),
                ('is_repeatable', models.BooleanField(default=True, verbose_name='Дозволити пройти модерацію ще раз?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical events',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='UsersFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=1024, validators=[django.core.validators.MinLengthValidator(64)])),
                ('main_photo', models.ImageField(blank=True, null=True, upload_to='events/reports/')),
                ('additional_photo', models.ImageField(blank=True, null=True, upload_to='events/reports/')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersfeedback', to='events.events')),
            ],
        ),
    ]
