# Generated by Django 3.2.16 on 2024-07-01 17:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalevents',
            name='creator',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Власник'),
        ),
        migrations.AddField(
            model_name='historicalevents',
            name='event_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='events.eventtypes', verbose_name='Тип події'),
        ),
        migrations.AddField(
            model_name='historicalevents',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='events',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL, verbose_name='Власник'),
        ),
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
        migrations.AddField(
            model_name='events',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.eventtypes', verbose_name='Тип події'),
        ),
        migrations.AddField(
            model_name='eventreports',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events'),
        ),
        migrations.AddField(
            model_name='eventreports',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventreporttypes'),
        ),
        migrations.AddField(
            model_name='eventimgs',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventimgs', to='events.events'),
        ),
        migrations.AddField(
            model_name='eventguests',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.events'),
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
        migrations.AlterUniqueTogether(
            name='eventguests',
            unique_together={('event', 'guest')},
        ),
    ]
