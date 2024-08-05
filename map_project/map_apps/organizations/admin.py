from django.contrib import admin

from .models import (OrganizationImgs, OrganizationLinks, Organizations,
                     OrgTypes)

# Register your models here.

admin.site.register(Organizations)
admin.site.register(OrgTypes)
admin.site.register(
    OrganizationLinks,
)
admin.site.register(OrganizationImgs)
