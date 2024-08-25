from django.utils import timezone

from ..models import Events


class TimeProvider:
    def get_local_time(self):
        return timezone.localtime(timezone.now())


class EventList:
    def __init__(self, result_revue="approved", exclude="ended"):
        self.result_revue = result_revue
        self.exclude = exclude

    def get_events_to_update(self, current_day, current_time):
        events = Events.objects.filter(
            result_revue=self.result_revue,
            begin_day=current_day,
            begin_time__lte=current_time,
        ).exclude(event_status=self.exclude)
        return events


class EventUpdater:
    def __init__(self, event_list: object, time_provider: object):
        self.event_list = event_list
        self.time_provider = time_provider

    def event_update(self):
        localtime = self.time_provider.get_local_time()
        current_time = localtime.time()
        current_day = localtime.date()

        events = self.event_list.get_events_to_update(
            current_day=current_day, current_time=current_time
        )

        for event in events:
            if event.end_time <= current_time:
                event.event_status = "ended"
            else:
                event.event_status = "in_process"
            event.save()
