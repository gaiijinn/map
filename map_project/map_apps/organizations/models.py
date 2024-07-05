from django.db import models

from ..users.models import User

# Create your models here.


class OrgTypes(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"Тип организации - {self.name}"


class Organizations(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="organizations"
    )
    org_type = models.ForeignKey(to=OrgTypes, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256, null=True, blank=True)
    about_us = models.CharField(max_length=512, null=True, blank=True)


class OrganizationImgs(models.Model):
    """For many imgs in one org profile"""

    org = models.ForeignKey(
        to=Organizations, on_delete=models.CASCADE, related_name="organizationimgs"
    )
    photo = models.ImageField(upload_to="org/")


class OrganizationLinks(models.Model):
    """For many links in one org profile"""

    SOCIAL_MEDIA_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("linkedin", "LinkedIn"),
        ("instagram", "Instagram"),
        ("website", "Website"),
        ("other", "Other"),
    ]

    org = models.ForeignKey(
        to=Organizations, on_delete=models.CASCADE, related_name="organizationlinks"
    )
    link_type = models.CharField(
        max_length=20, choices=SOCIAL_MEDIA_CHOICES, default="other"
    )
    link = models.URLField(max_length=256)
