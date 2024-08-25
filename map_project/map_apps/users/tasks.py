from celery import shared_task
from django.db.models import Sum
from django.contrib.auth import get_user_model


@shared_task
def level_calculating(user_id: int):
    from ..achievements.models import AchievementsProgressStatus
    from .models import UserLevel, UserProfile

    user = get_user_model().objects.select_related("user_profile").filter(id=user_id).first()

    if user:
        total_exp = (
            AchievementsProgressStatus.objects.select_related("achievement")
            .filter(user=user, is_achieved=True)
            .aggregate(total_exp=Sum("achievement__given_exp"))["total_exp"]
            or 0
        )

        current_level = UserLevel.objects.filter(
            low_range__lte=total_exp, top_range__gte=total_exp
        ).first()

        if current_level:
            UserProfile.objects.filter(user=user).update(user_level=current_level)
