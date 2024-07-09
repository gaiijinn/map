# Generated by Django 3.2.16 on 2024-07-08 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userverification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userverification', to=settings.AUTH_USER_MODEL, verbose_name='Користувач'),
        ),
    ]
