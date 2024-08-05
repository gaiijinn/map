from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import CreatorSubscriptions, User, UserLevel, UserProfile
admin.site.register(User)
admin.site.register(UserLevel)
admin.site.register(UserProfile, SimpleHistoryAdmin)
admin.site.register(CreatorSubscriptions)
