from celery import shared_task
from django.utils import timezone

from .models import Events
from .services import send_approved_event_email, send_reject_event_email


@shared_task
def task_event_email(event_id: int):
    event = Events.objects.filter(id=event_id).first()
    if event:
        if event.result_revue == "rejected":
            send_reject_event_email(event)
        elif event.result_revue == "approved":
            send_approved_event_email(event)


@shared_task()
def check_status_events():
    localtime = timezone.localtime(timezone.now())
    current_time = localtime.time()
    current_day = localtime.date()

    events = Events.objects.filter(result_revue='approved', event_status='not_started', begin_day=current_day,
                                   begin_time__lte=current_time)

    if events:
        for event in events:
            event.event_status = 'in_process'
            event.save()
