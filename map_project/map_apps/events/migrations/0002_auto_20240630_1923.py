# Generated by Django 3.2.16 on 2024-06-30 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='event_guests',
            field=models.ManyToManyField(related_name='event_guests', through='events.EventGuests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='events',
            name='event_reports',
            field=models.ManyToManyField(related_name='event_reports', through='events.EventReports', to='events.EventReportTypes'),
        ),
        migrations.AlterField(
            model_name='eventguests',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events'),
        ),
        migrations.AlterField(
            model_name='eventguests',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='eventreports',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events'),
        ),
        migrations.AlterField(
            model_name='eventreports',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventreporttypes'),
        ),
    ]
