from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Events, EventGuests, UnverifiedEvents, RejectedEvents


@receiver(post_save, sender=Events)
def after_saving_manipulate(sender, instance, created, **kwargs):
    if created:
        if instance.creator.is_org:
            instance.created_by_org = True
            instance.save()

        UnverifiedEvents.objects.create(event=instance)
        EventGuests.objects.create(event=instance, guest=instance.creator)
    else:
        rejected_event = (RejectedEvents.objects
                          .filter(event__result_revue='Відмова', event__event=instance)
                          .order_by('-unverified_date')
                          .first())

        if rejected_event and rejected_event.event.is_repeatable:
            UnverifiedEvents.objects.create(event=instance)
