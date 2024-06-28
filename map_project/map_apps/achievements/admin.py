from django.contrib import admin

from .models import Achievements, AchievementsProgressStatus

# Register your models here.

admin.site.register(Achievements)
admin.site.register(AchievementsProgressStatus)
