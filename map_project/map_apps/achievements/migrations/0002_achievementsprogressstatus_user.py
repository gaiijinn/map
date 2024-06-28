# Generated by Django 3.2.16 on 2024-06-28 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievementsprogressstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievementsprogressstatus', to=settings.AUTH_USER_MODEL),
        ),
    ]