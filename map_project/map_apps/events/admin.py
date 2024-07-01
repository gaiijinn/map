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
    search_fields = ('event__name', )

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = Events._meta.get_field('name').verbose_name

    def event_type(self, obj):
        return obj.event.event_type.name
    event_type.short_description = Events._meta.get_field('event_type').verbose_name

    def event_age(self, obj):
        return obj.event.event_age
    event_age.short_description = Events._meta.get_field('event_age').verbose_name

    def event_price(self, obj):
        return obj.event.price
    event_price.short_description = Events._meta.get_field('price').verbose_name

    def event_begin_day(self, obj):
        return obj.event.begin_day
    event_begin_day.short_description = Events._meta.get_field('begin_day').verbose_name

    def event_begin_time(self, obj):
        return obj.event.begin_time
    event_begin_time.short_description = Events._meta.get_field('begin_time').verbose_name

    def event_end_time(self, obj):
        return obj.event.end_time
    event_end_time.short_description = Events._meta.get_field('end_time').verbose_name

    def name(self, obj):
        return obj.event.name
    name.short_description = Events._meta.get_field('name').verbose_name

    def address(self, obj):
        return obj.event.address
    address.short_description = Events._meta.get_field('address').verbose_name

    def description(self, obj):
        return obj.event.description
    description.short_description = Events._meta.get_field('description').verbose_name

    def created_by_org(self, obj):
        return obj.event.created_by_org
    created_by_org.short_description = Events._meta.get_field('created_by_org').verbose_name

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
