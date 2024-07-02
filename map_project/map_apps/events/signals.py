from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Events, EventGuests, EventStatusEmail
from .tasks import task_reject_event_email
from django.utils.timezone import now


@receiver(post_save, sender=Events)
def after_saving_manipulate(sender, instance, created, **kwargs):
    if created:
        if instance.creator.is_org:
            instance.created_by_org = True
            instance.save()
        EventGuests.objects.create(event=instance, guest=instance.creator)


@receiver(post_save, sender=EventStatusEmail)
def event_status_email(sender, instance, created, **kwargs):
    if created:
        task_reject_event_email.delay(instance.event.id)
