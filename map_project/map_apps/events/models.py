from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from ..users.models import User, UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

# Create your models here.


class EventGuests(models.Model):
    event = models.ForeignKey("Events", on_delete=models.CASCADE, related_name='eventguests')
    guest = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.name} | {self.guest.get_full_name()}"


class EventReportTypes(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.name}"


class EventReports(models.Model):
    event = models.ForeignKey("Events", on_delete=models.CASCADE, related_name='eventreports')
    report = models.ForeignKey(EventReportTypes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.name} | {self.user.get_full_name()} - {self.report.name}"


class EventType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"{self.name}"


class EventTypes(models.Model):
    event = models.ForeignKey("Events", on_delete=models.CASCADE, related_name='eventtypes')
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.name} | {self.event_type.name}"


class EventStatusEmail(models.Model):
    """Model to track if event status was emailed to user only 1 time"""

    event = models.ForeignKey(
        "Events",
        on_delete=models.CASCADE,
        related_name="eventstatusemail",
        verbose_name="Подія",
    )
    status = models.CharField(_("Статус події"), max_length=64)
    feedback = models.CharField(max_length=1024, null=True, default="")

    def __str__(self):
        return f"{self.event.name} | {self.status}"


class Events(models.Model):
    EVENT_STATUS_CHOICES = (
        ("not_started", "Не почато"),
        ("in_process", "Проходить"),
        ("ended", "Завершилось"),
    )

    EVENT_AGE_CHOICES = (
        ("+0", "+0"),
        ("+6", "+6"),
        ("+12", "+12"),
        ("+16", "+16"),
        ("+18", "+18"),
    )

    STATUS_REVUE = (
        ("Підтверджено", "Підтверджено"),
        ("Відмова", "Відмова"),
        ("На перевірці", "На перевірці"),
    )

    creator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="created_events",
        verbose_name=_("Власник"),
    )

    event_types = models.ManyToManyField(
        EventType,
        through=EventTypes,
        verbose_name=_("Тип події"),
    )

    event_guests = models.ManyToManyField(
        User, through=EventGuests
    )
    event_reports = models.ManyToManyField(
        EventReportTypes, through=EventReports
    )

    event_status = models.CharField(
        _("Статус події"),
        choices=EVENT_STATUS_CHOICES,
        default="not_started",
        max_length=32,
        db_index=True,
    )
    event_age = models.CharField(
        _("Вікові обмеження"),
        choices=EVENT_AGE_CHOICES,
        default="+0",
        max_length=4,
        db_index=True,
    )

    begin_day = models.DateField(_("День проведення"))
    begin_time = models.TimeField(_("Час початку проведення події"))
    end_time = models.TimeField(_("Час кінця проведення події"))

    name = models.CharField(_("Назва події"), max_length=256, db_index=True)
    address = models.CharField(_("Адреса проведення"), max_length=256)
    description = models.CharField(_("Опис події"), max_length=512)

    main_photo = models.ImageField(upload_to='events/created/')
    coordinates = models.JSONField(_("Координати"))
    price = models.PositiveSmallIntegerField(_("Ціна за вхід"), blank=True, default=0)
    created_by_org = models.BooleanField(_("Створено організацією?"), default=False)

    # for admin
    result_revue = models.CharField(
        _("Статус перевірки"),
        choices=STATUS_REVUE,
        default="На перевірці",
        max_length=64,
        db_index=True,
    )
    feedback = models.CharField(
        _("Відгук модератора"), max_length=1024, blank=True, null=True
    )
    created_at = models.DateTimeField(_("Подію створено"), auto_now_add=True)
    last_time_updated = models.DateTimeField(
        _("Подію редаговано"), null=True, blank=True
    )
    is_repeatable = models.BooleanField(
        _("Дозволити пройти модерацію ще раз?"), default=True
    )

    history = HistoricalRecords()

    def clean(self):
        """Validation before saving object"""
        super().clean()
        if self.begin_time >= self.end_time:
            raise ValidationError(
                {
                    "end_time": _(
                         "Час кінця події повинен буде більшим за початок"
                    )
                }
            )
        if self.result_revue == "Відмова" and self.feedback is None:
            raise ValidationError(
                {
                    "feedback": _(
                        "Результат перевірки при відмові не повинен бути пустим!"
                    )
                }
            )

    class Meta:
        indexes = [
            models.Index(fields=["event_status", "event_age"]),
        ]

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.result_revue != "На перевірці":
            """To send uniq emails status/feedback to user email"""
            obj, created = EventStatusEmail.objects.get_or_create(
                event=self, status=self.result_revue, feedback=self.feedback
            )
        return super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )


class EventImgs(models.Model):
    event = models.ForeignKey(
        to=Events, on_delete=models.CASCADE, related_name="eventimgs"
    )
    img = models.ImageField(upload_to="events")


class UsersFeedback(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='usersfeedback')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='usersfeedback')
    feedback = models.CharField(max_length=1024, validators=[MinLengthValidator(64)])
    main_photo = models.ImageField(upload_to='events/reports/', blank=True, null=True)
    additional_photo = models.ImageField(upload_to='events/reports/', blank=True, null=True )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    #datetime = models.DateTimeField(auto_now_add=True)
