# Generated by Django 3.2.16 on 2024-07-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_eventstatusemail"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventstatusemail",
            name="feedback",
            field=models.CharField(default="", max_length=1024, null=True),
        ),
    ]