from django.db import models
from ..users.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

# Create your models here.


class EventGuests(models.Model):
    event = models.ForeignKey('Events', on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'guest')

    def __str__(self):
        return f"{self.event.name} | {self.guest.get_full_name()}"


class EventReportTypes(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'


class EventReports(models.Model):
    event = models.ForeignKey('Events', on_delete=models.CASCADE)
    report = models.ForeignKey(EventReportTypes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} | {self.report.name}"


class EventTypes(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'


class Events(models.Model):
    EVENT_STATUS_CHOICES = (
        ('not_started', 'Не почато'),
        ('in_process', 'Проходить'),
        ('ended', 'Завершилось'),
    )

    EVENT_AGE_CHOICES = (
        ('+0', '+0'),
        ('+6', '+6'),
        ('+12', '+12'),
        ('+16', '+16'),
        ('+18', '+18'),
    )

    STATUS_REVUE = (
        ('Підтверджено', 'Підтверджено'),
        ('Відмова', 'Відмова'),
        ('На перевірці', 'На перевірці'),
    )

    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='events', verbose_name=_('Власник'))
    event_type = models.ForeignKey(to=EventTypes, on_delete=models.CASCADE, related_name='events',
                                   verbose_name=_('Тип події'))

    event_guests = models.ManyToManyField(User, through=EventGuests, related_name='event_guests')
    event_reports = models.ManyToManyField(EventReportTypes, through=EventReports, related_name='event_reports')

    event_status = models.CharField(_("Статус події"), choices=EVENT_STATUS_CHOICES, default='not_started',
                                    max_length=32, db_index=True)
    event_age = models.CharField(_("Вікові обмеження"), choices=EVENT_AGE_CHOICES, default='+0', max_length=4,
                                 db_index=True)

    begin_day = models.DateField(_("День проведення"))
    begin_time = models.TimeField(_("Час початку проведення події"))
    end_time = models.TimeField(_("Час кінця проведення події"))

    name = models.CharField(_("Назва події"), max_length=256, db_index=True)
    address = models.CharField(_("Адреса проведення"), max_length=256)
    description = models.CharField(_("Опис події"), max_length=512)
    coordinates = models.JSONField(_("Координати"))
    price = models.PositiveSmallIntegerField(_("Ціна за вхід"), blank=True, default=0)
    created_by_org = models.BooleanField(_("Створено організацією?"), default=False)

    # for admin
    result_revue = models.CharField(_("Статус перевірки"), choices=STATUS_REVUE, default='На перевірці',
                                    max_length=64, db_index=True)
    feedback = models.CharField(_("Відгук модератора"), max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(_("Подію створено"), auto_now_add=True)
    last_time_updated = models.DateTimeField(_("Подію редаговано"), null=True, blank=True)
    is_repeatable = models.BooleanField(_("Дозволити пройти модерацію ще раз?"), default=True)

    history = HistoricalRecords()

    def clean(self):
        """Validation before saving object"""
        super().clean()
        if self.begin_time and self.end_time and self.begin_time >= self.end_time:
            raise ValidationError({
                'end_time': _('Час кінця події повинен буде більшим за початок')
            })

    class Meta:
        indexes = [
            models.Index(fields=['event_status', 'event_age']),
        ]


class EventImgs(models.Model):
    event = models.ForeignKey(to=Events, on_delete=models.CASCADE, related_name='eventimgs')
    img = models.ImageField(upload_to='events')

