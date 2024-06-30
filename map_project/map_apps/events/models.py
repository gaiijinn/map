from django.db import models
from ..users.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


class EventReportTypes(models.Model):
    name = models.CharField(max_length=128, unique=True)


class EventTypes(models.Model):
    name = models.CharField(max_length=128, unique=True)


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

    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='events')
    event_type = models.ForeignKey(to=EventTypes, on_delete=models.CASCADE, related_name='events')

    event_status = models.CharField(choices=EVENT_STATUS_CHOICES, default='not_started', max_length=32)
    event_age = models.CharField(choices=EVENT_AGE_CHOICES, default='+0', max_length=4)

    begin_day = models.DateField()
    begin_time = models.TimeField()
    end_time = models.TimeField()

    address = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    coordinates = models.JSONField()
    price = models.PositiveSmallIntegerField(blank=True, default=0)
    created_by_org = models.BooleanField(default=False)

    # def clean(self):
    #     """Validation before saving object"""
    #     super().clean()
    #     if self.begin_time and self.end_time and self.begin_time >= self.end_time:
    #         raise ValidationError({
    #             'end_time': _('Час кінця події повинен буде більшим за початок')
    #         })


class EventReports(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='eventreports')
    report = models.ForeignKey(EventReportTypes, on_delete=models.CASCADE, related_name='eventreports')


class EventGuests(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='eventguests')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventguests')

    class Meta:
        unique_together = ('event', 'guest')


class EventImgs(models.Model):
    event = models.ForeignKey(to=Events, on_delete=models.CASCADE, related_name='eventimgs')
    img = models.ImageField(upload_to='events')


class UnverifiedEvents(models.Model):
    """Model to moderate events"""
    STATUS_RESULT = (
        ('aproved', 'Підтверджено'),
        ('not_aproved', 'Не підтверджено'),
        ('in_revue', 'На перевірці'),
    )

    event = models.ForeignKey(to=Events, on_delete=models.CASCADE, related_name='unverifiedevents')
    result_revue = models.CharField(choices=STATUS_RESULT, default='in_revue', max_length=64)

    recieved = models.DateTimeField(auto_now_add=True)
    verified_date = models.DateTimeField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.result_revue == 'aproved':
            pass
        if self.result_revue == 'not_aproved':
            pass
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
