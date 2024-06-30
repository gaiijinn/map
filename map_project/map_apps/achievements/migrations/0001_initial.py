# Generated by Django 3.2.16 on 2024-06-30 20:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement_name', models.CharField(max_length=128)),
                ('descr_achievement', models.CharField(blank=True, max_length=256)),
                ('given_exp', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('final_value', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('for_organization', models.BooleanField(default=False)),
                ('for_def_user', models.BooleanField(default=True)),
                ('achievement_image', models.ImageField(blank=True, upload_to='achiev_img/')),
            ],
        ),
        migrations.CreateModel(
            name='AchievementsProgressStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_rn', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_achieved', models.BooleanField(default=False)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievementsprogressstatus', to='achievements.achievements')),
            ],
        ),
    ]
