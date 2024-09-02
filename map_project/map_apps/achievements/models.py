from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ..users.models import User

# Create your models here.


class Achievements(models.Model):
    """Models to save the achievements"""

    ACHIEVEMENT_KEYWORD = (
        ('DV', 'default_value'),
        ('UP', 'update_profile'),
        ('CE', 'create_event'),
        ('CS', 'create_subscription'),
    )

    achievement_name = models.CharField(max_length=128)
    keyword = models.CharField(choices=ACHIEVEMENT_KEYWORD, max_length=128, default='DV')
    descr_achievement = models.CharField(max_length=256, blank=True)
    given_exp = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    final_value = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(1)]
    )
    for_organization = models.BooleanField(default=False)
    for_def_user = models.BooleanField(default=True)
    achievement_image = models.ImageField(upload_to="achiev_img/", blank=True)

    def __str__(self):
        return f"{self.achievement_name}"


class AchievementsProgressStatus(models.Model):
    """Models to track the user achievements progres"""

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="achievementsprogressstatus"
    )
    achievement = models.ForeignKey(
        to=Achievements,
        on_delete=models.CASCADE,
        related_name="achievementsprogressstatus",
    )
    progress_rn = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.user.get_full_name()} | {self.achievement.achievement_name} | Виконано = {self.is_achieved}, "
            f"{self.progress_rn}/{self.achievement.final_value}"
        )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.progress_rn > self.achievement.final_value:
            self.progress_rn = self.achievement.final_value
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
