from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EventGuests, Events, EventStatusEmail
from .tasks import send_email_to_subscribers, task_event_email


@receiver(post_save, sender=Events)
def after_saving_manipulate(sender, instance, created, **kwargs):
    if created:
        if instance.creator.is_org:
            instance.created_by_org = True
            instance.save()
        EventGuests.objects.create(event=instance, guest=instance.creator)
    else:
        if instance.result_revue == "approved":
            send_email_to_subscribers.delay(instance.id)


@receiver(post_save, sender=EventStatusEmail)
def event_status_email(sender, instance, created, **kwargs):
    """Send only uniq emails, like different status, feedback from admin"""
    if created:
        task_event_email.delay(instance.event.id)
