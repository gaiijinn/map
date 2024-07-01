from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Events, EventGuests
from .tasks import task_reject_event_email
from django.utils.timezone import now


@receiver(post_save, sender=Events)
def after_saving_manipulate(sender, instance, created, **kwargs):
    if created:
        if instance.creator.is_org:
            instance.created_by_org = True
            instance.save()
        EventGuests.objects.create(event=instance, guest=instance.creator)
    else:
        if instance.result_revue != 'На перевірці':
            task_reject_event_email.delay(instance.id)
