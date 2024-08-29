from django.utils import timezone

from ..models import Events


class TimeProvider:
    """
    Just getting our server timezone
    """

    def get_local_time(self):
        return timezone.localtime(timezone.now())


class EventList:
    """
    This class is responsible to return the filtered event depends on local time and day, also init takes
    two important arguments. 'result_revue' is the Event model field, it shows if event was moderated successfully.
    """

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
    """
    Updates the status of events based on the current local time and day.

    Retrieves the current local time and day using the TimeProvider instance, then gets the events
    to update from the EventList instance. For each event, updates its status to "ended" if its
    end time has passed, or to "in_process" if it is still ongoing. Saves the updated event status
    to the database.
    """

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
