from celery import shared_task

from .models import Events
from .services.event_service import TimeProvider, EventList, EventUpdater
from .services.email_service import EmailController


@shared_task
def task_event_email(event_id: int):
    event = Events.objects.filter(id=event_id).first()
    if event:
        email_controller = EmailController(event)
        recipient_list = [event.creator.email]
        email_controller.send_email(recipient_list)


@shared_task()
def check_status_events():
    """Task to set actual status event by current local time and event begin_time/end_time"""
    time_provider = TimeProvider()
    event_repository = EventList()

    updater = EventUpdater(time_provider=time_provider, event_list=event_repository)
    updater.event_update()
