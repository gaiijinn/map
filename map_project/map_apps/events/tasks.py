from celery import shared_task

from .models import Events
from .services import send_approved_event_email, send_reject_event_email


@shared_task
def task_reject_event_email(event_id: int):
    event = Events.objects.filter(id=event_id).first()
    if event:
        if event.result_revue == "Відмова":
            send_reject_event_email(event)
        elif event.result_revue == "Підтверджено":
            send_approved_event_email(event)