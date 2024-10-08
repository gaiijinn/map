from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserLevel(models.Model):
    """Model to calculate the user level by exp in achieved achievements"""

    level_name = models.CharField(max_length=128)
    low_range = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    top_range = models.PositiveSmallIntegerField()

    def clean(self):
        """Validation for the level range"""
        if self.low_range > self.top_range or self.low_range == self.top_range:
            raise ValidationError(
                {
                    "top_range": "Число верхньої границі повинно бути більшою за меншу границю"
                }
            )

    def __str__(self):
        return f"{self.level_name}"

    class Meta:
        verbose_name = "Тип рівня користувача"
        verbose_name_plural = "Рівні користувачів"


class User(AbstractUser):
    """Updated user model"""

    username = None
    email = models.EmailField(_("Електронна адреса"), unique=True)

    is_org = models.BooleanField(
        _("Зареєстрований як організація"), default=False, db_index=True
    )
    rating = models.PositiveSmallIntegerField(_("Рейтинг"), default=0, blank=True)

    subscriptions = models.ManyToManyField(
        to='self',
        through='UserSubscription',
        symmetrical=False,
        related_name='subscribed_to',
        blank=True,
    )

    profile_picture = models.ImageField(
        _("Фото користувача"),
        upload_to="users/profile_picture/",
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        if not full_name.strip():
            full_name = self.email

        return full_name

    class Meta:
        verbose_name = "Користувача"
        verbose_name_plural = "Користувачі"


class UserProfile(models.Model):
    """Models to save the user additional info"""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_profile",
        verbose_name=_("Користувач"),
    )
    user_level = models.ForeignKey(
        to=UserLevel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Рівень користувача"),
    )
    about_me = models.CharField(_("Про себе"), max_length=512, blank=True, null=True)
    inst_link = models.URLField(
        _("Instagram посилання"), max_length=256, blank=True, null=True
    )
    want_newsletters = models.BooleanField(_("Згоден отримувати новини"), default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.get_full_name()} | {self.user_level}"


class UserSubscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions_made'
    )
    subscribe_to = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions_received'
    )
    subscribe_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'subscribe_to')
        indexes = [
            models.Index(fields=['user', 'subscribe_to'])
        ]
