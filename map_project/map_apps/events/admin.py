from django.contrib import admin
from .models import (EventTypes, Events, EventGuests, EventReportTypes, EventReports, EventImgs, UnverifiedEvents,
                     VerifiedEvents, RejectedEvents)

# Register your models here.

admin.site.register(EventTypes)
admin.site.register(Events)
admin.site.register(EventGuests)
admin.site.register(EventImgs)

admin.site.register(EventReportTypes)
admin.site.register(EventReports)

admin.site.register(UnverifiedEvents)
admin.site.register(VerifiedEvents)
admin.site.register(RejectedEvents)
