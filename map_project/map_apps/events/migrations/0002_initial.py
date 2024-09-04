# Generated by Django 3.2.16 on 2024-09-04 14:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersfeedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersfeedback', to='users.userprofile'),
        ),
        migrations.AddField(
            model_name='historicalevents',
            name='creator',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Власник'),
        ),
        migrations.AddField(
            model_name='historicalevents',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventtypes',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventtypes', to='events.events'),
        ),
        migrations.AddField(
            model_name='eventtypes',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventtype'),
        ),
        migrations.AddField(
            model_name='eventstatusemail',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventstatusemail', to='events.events', verbose_name='Подія'),
        ),
        migrations.AddField(
            model_name='events',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to=settings.AUTH_USER_MODEL, verbose_name='Власник'),
        ),
        migrations.AddField(
            model_name='events',
            name='event_guests',
            field=models.ManyToManyField(through='events.EventGuests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='events',
            name='event_reports',
            field=models.ManyToManyField(through='events.EventReports', to='events.EventReportTypes'),
        ),
        migrations.AddField(
            model_name='events',
            name='event_types',
            field=models.ManyToManyField(through='events.EventTypes', to='events.EventType', verbose_name='Тип події'),
        ),
        migrations.AddField(
            model_name='eventreports',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventreports', to='events.events'),
        ),
        migrations.AddField(
            model_name='eventreports',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventreporttypes'),
        ),
        migrations.AddField(
            model_name='eventreports',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventimgs',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventimgs', to='events.events'),
        ),
        migrations.AddField(
            model_name='eventguests',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventguests', to='events.events'),
        ),
        migrations.AddField(
            model_name='eventguests',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='events',
            index=models.Index(fields=['event_status', 'event_age'], name='events_even_event_s_0a67fc_idx'),
        ),
    ]