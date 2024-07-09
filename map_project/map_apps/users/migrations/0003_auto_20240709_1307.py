# Generated by Django 3.2.16 on 2024-07-09 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userverification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverification',
            name='expired_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дійсний до'),
        ),
        migrations.AlterField(
            model_name='userverification',
            name='verif_to',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Активовано до'),
        ),
    ]