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

admin.site.register(VerifiedEvents)


@admin.register(UnverifiedEvents)
class UnverifiedEventsAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'recieved', 'result_revue')
    list_select_related = ('event', )
    readonly_fields = ('event_name', 'event_type', 'event_age', 'event_price',
                       'event_begin_day', 'event_begin_time', 'event_end_time',
                       'name', 'address', 'description', 'created_by_org')
    ordering = ('recieved', )
    list_filter = ('result_revue', 'recieved')
    search_fields = ('event_name', )

    def event_name(self, obj):
        return obj.event.name

    def event_type(self, obj):
        return obj.event.event_type.name

    def event_age(self, obj):
        return obj.event.event_age

    def event_price(self, obj):
        return obj.event.price

    def event_begin_day(self, obj):
        return obj.event.begin_day

    def event_begin_time(self, obj):
        return obj.event.begin_time

    def event_end_time(self, obj):
        return obj.event.end_time

    def name(self, obj):
        return obj.event.name

    def address(self, obj):
        return obj.event.address

    def description(self, obj):
        return obj.event.description

    def created_by_org(self, obj):
        return obj.event.created_by_org

    fieldsets = (
        ('Подія основа', {
            'fields': ('event_name', 'event_type', 'event_price'),
            'classes': ('wide',),
        }),
        ('Вік', {
            'fields': ('event_age',),
            'classes': ('wide',),
        }),
        ('Час', {
            'fields': ('event_begin_day', 'event_begin_time', 'event_end_time'),
            'classes': ('wide',),
        }),
        ('Додатково', {
            'fields': ('name', 'address', 'description', 'created_by_org'),
            'classes': ('wide',),
        }),
        ('Відгук', {
            'fields': ('result_revue', 'is_repeatable', 'feedback'),
            'classes': ('wide',),
        }),
    )


@admin.register(RejectedEvents)
class RejectedEventsAdmin(admin.ModelAdmin):
    ordering = ('unverified_date',)
    search_fields = ('event__event__name',)
    list_filter = ('unverified_date', 'event__is_repeatable', 'event__event__event_type')

    list_select_related = ('event__event', 'event__event__event_type')

    list_display = ('event_name', 'unverified_date', 'event_is_repeatable', 'event_type')
    readonly_fields = ('event_name', 'event_type', 'event_price', 'event_reject_feedback', 'event_is_repeatable')

    def event_name(self, obj):
        return obj.event.event.name

    def event_type(self, obj):
        return obj.event.event.event_type.name

    def event_price(self, obj):
        return obj.event.event.price

    def event_is_repeatable(self, obj):
        return obj.event.is_repeatable

    def event_reject_feedback(self, obj):
        return obj.event.feedback


    fieldsets = (
        ('Основні дані', {
            'fields': ('event_name', 'event_type', 'event_price'),
            'classes': ('wide',),
        }),
        ('Причина відмови', {
            'fields': ('event_reject_feedback', 'event_is_repeatable'),
            'classes': ('wide',),
        }),
    )
