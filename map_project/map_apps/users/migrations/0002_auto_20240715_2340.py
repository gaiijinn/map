# Generated by Django 3.2.16 on 2024-07-15 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='subscriptions',
        ),
        migrations.DeleteModel(
            name='UserSubscriptions',
        ),
    ]
