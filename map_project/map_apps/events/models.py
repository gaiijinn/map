from django.db import models
from ..users.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='events', verbose_name=_('Власник'))
    event_type = models.ForeignKey(to=EventTypes, on_delete=models.CASCADE, related_name='events',
                                   verbose_name=_('Тип події'))

    event_guests = models.ManyToManyField(User, through=EventGuests, related_name='event_guests')
    event_reports = models.ManyToManyField(EventReportTypes, through=EventReports, related_name='event_reports')

    event_status = models.CharField(_("Статус події"), choices=EVENT_STATUS_CHOICES, default='not_started', max_length=32, db_index=True)
    event_age = models.CharField(_("Вікові обмеження"), choices=EVENT_AGE_CHOICES, default='+0', max_length=4, db_index=True)

    begin_day = models.DateField(_("День проведення"))
    begin_time = models.TimeField(_("Час початку проведення події"))
    end_time = models.TimeField(_("Час кінця проведення події"))

    name = models.CharField(_("Назва події"), max_length=256, db_index=True)
    address = models.CharField(_("Адреса проведення"), max_length=256)
    description = models.CharField(_("Опис події"), max_length=512)
    coordinates = models.JSONField(_("Координати"))
    price = models.PositiveSmallIntegerField(_("Ціна за вхід"), blank=True, default=0)
    created_by_org = models.BooleanField(_("Створено організацією?"), default=False)

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


class VerifiedEvents(models.Model):
    """From here we take all events to put it on map"""
    event = models.ForeignKey(to=Events, on_delete=models.CASCADE)
    verified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name}"


class RejectedEvents(models.Model):
    """If rejected event can be repeatable """
    event = models.ForeignKey(to='UnverifiedEvents', on_delete=models.CASCADE)
    unverified_date = models.DateTimeField(auto_now_add=True)


class UnverifiedEvents(models.Model):
    """Model to moderate events"""
    STATUS_RESULT = (
        ('Підтверджено', 'Підтверджено'),
        ('Відмова', 'Відмова'),
        ('На перевірці', 'На перевірці'),
    )

    event = models.ForeignKey(to=Events, on_delete=models.CASCADE)
    result_revue = models.CharField(choices=STATUS_RESULT, default='На перевірці', max_length=64)

    recieved = models.DateTimeField(auto_now_add=True)
    is_repeatable = models.BooleanField(default=True)
    feedback = models.CharField(max_length=1024, blank=True, null=True)
    #надо добавить приоритет фолс чтобы когда чел отредал ивент модеры быстрее его обработали

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.result_revue == 'Підтверджено':
            VerifiedEvents.objects.create(event=self.event)
            #self.delete()
        if self.result_revue == 'Відмова':
            if not RejectedEvents.objects.filter(event=self).exists():
                RejectedEvents.objects.create(event=self)
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f"{self.event.name} | {self.result_revue}"
