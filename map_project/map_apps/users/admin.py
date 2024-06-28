from django.contrib import admin

from .models import User, UserLevel, UserProfile, UserVerification

admin.site.register(User)
admin.site.register(UserLevel)
admin.site.register(UserProfile)
admin.site.register(UserVerification)
