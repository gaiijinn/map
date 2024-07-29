# Generated by Django 3.2.16 on 2024-07-17 16:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_auto_20240717_1917"),
        ("events", "0003_auto_20240715_2330"),
    ]

    operations = [
        migrations.AlterField(
            model_name="events",
            name="main_photo",
            field=models.ImageField(upload_to="events/created/"),
        ),
        migrations.CreateModel(
            name="UsersFeedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "feedback",
                    models.CharField(
                        max_length=1024,
                        validators=[django.core.validators.MinLengthValidator(64)],
                    ),
                ),
                (
                    "main_photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="events/reports/"
                    ),
                ),
                (
                    "additional_photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="events/reports/"
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usersfeedback",
                        to="events.events",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usersfeedback",
                        to="users.userprofile",
                    ),
                ),
            ],
        ),
    ]
