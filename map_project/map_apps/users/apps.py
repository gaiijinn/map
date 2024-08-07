from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "map_apps.users"

    def ready(self):
        from ..users import signals
