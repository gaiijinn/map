from django.apps import AppConfig


class AchievementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'map_apps.achievements'

    def ready(self):
        from ..achievements import signals
