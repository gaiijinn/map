# Generated by Django 3.2.16 on 2024-08-03 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='main_photo',
            field=models.ImageField(upload_to='events/created/', verbose_name='Зображення заставки'),
        ),
        migrations.AlterField(
            model_name='historicalevents',
            name='main_photo',
            field=models.TextField(max_length=100, verbose_name='Зображення заставки'),
        ),
    ]
