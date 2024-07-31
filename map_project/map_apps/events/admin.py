from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    EventGuests,
    EventImgs,
    EventReports,
    EventReportTypes,
    Events,
    EventStatusEmail,
    EventType,
    EventTypes,
    UsersFeedback,
)

# Register your models here.

admin.site.register(EventTypes)
admin.site.register(EventType)
admin.site.register(EventGuests)
admin.site.register(EventImgs)

admin.site.register(EventReportTypes)
admin.site.register(EventReports)
admin.site.register(EventStatusEmail)

admin.site.register(UsersFeedback)


class EventsHistoryAdmin(SimpleHistoryAdmin):
    list_display = (
        "name",
        "result_revue",
        "created_by_org",
        "created_at",
        "last_time_updated",
        "is_repeatable",
    )
    search_fields = ("name",)
    list_filter = ("created_at", "result_revue", "is_repeatable", "created_by_org")
    readonly_fields = ("created_at", "display_images", "display_event_types")

    history_list_display = ("result_revue", "feedback")

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "price",
                    "event_age",
                    "creator",
                    "created_at",
                    "main_photo",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Данные о начале",
            {
                "fields": ("begin_day", "begin_time", "end_time"),
                "classes": ("wide",),
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": ("address", "description", "coordinates"),
                "classes": ("wide",),
            },
        ),
        (
            "Категории",
            {
                "fields": ("display_event_types",),
                "classes": ("wide",),
            },
        ),
        (
            "Добавлені автором фотографії",
            {
                "fields": ("display_images",),
                "classes": ("wide",),
            },
        ),
        (
            "Информация для администраторов",
            {
                "fields": (
                    "result_revue",
                    "feedback",
                    "last_time_updated",
                    "is_repeatable",
                ),
                "classes": ("wide",),
            },
        ),
    )

    def display_images(self, obj):
        images = obj.eventimgs.all()
        if images:
            return format_html(
                "<br>".join(
                    '<img src="{}" style="max-width: 300px; max-height: 300px; margin: 5px;"/>'.format(
                        img.img.url
                    )
                    for img in images
                )
            )
        return "Пусто"

    def display_event_types(self, obj):
        event_types = obj.event_types.all()
        if event_types:
            return format_html(
                "<br>".join(
                    "<p>{}</p>".format(event_type.name) for event_type in event_types
                )
            )
        return "Нет категорий"


admin.site.register(Events, EventsHistoryAdmin)
