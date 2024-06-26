import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now
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
            raise ValidationError({
                'top_range': 'Число верхньої границі повинно бути більшою за меншу границю'
            })

    def __str__(self):
        return f'{self.level_name}'

    class Meta:
        verbose_name = 'Тип рівня користувача'
        verbose_name_plural = 'Рівні користувачів'


class User(AbstractUser):
    """Updated user model"""
    username = None
    email = models.EmailField(_("Електронна адреса"), unique=True)

    is_org = models.BooleanField(_("Зареєстрований як організація"), default=False, db_index=True)
    is_verif = models.BooleanField(_("Верифікований"), default=False)
    rating = models.PositiveSmallIntegerField(_("Рейтинг"), default=0, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email.split('@')[0]

    class Meta:
        verbose_name = 'Користувача'
        verbose_name_plural = 'Користувачі'


class UserProfile(models.Model):
    """Models to save the user additional info"""
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='userprofile', verbose_name=_('Користувач'))
    profile_picture = models.ImageField(_("Фото користувача"), upload_to='users/profile_picture/',
                                        blank=True,)
    user_level = models.ForeignKey(to=UserLevel, on_delete=models.CASCADE, related_name='userprofile',
                                   blank=True, null=True, verbose_name=_('Рівень користувача'))
    about_me = models.CharField(_("Про себе"), max_length=512, blank=True, null=True)
    inst_link = models.URLField(_("Instagram посилання"), max_length=256, blank=True, null=True)
    want_newsletters = models.BooleanField(_("Згоден отримувати новини"), default=False)
    history = HistoricalRecords()


class UserVerification(models.Model):
    """Base email verif model with uuid4"""
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('Користувач'))
    code = models.UUIDField(_("Код"), default=uuid.uuid4)
    created_at = models.DateTimeField(_("Створено"), auto_now_add=True)
    expired_at = models.DateTimeField(_("Дійсний до"),)
    verif_to = models.DateTimeField(_("Активовано до"),)

    def check_if_expired(self):
        return True if now() < self.expired_at else False

    def check_if_verif(self):
        return True if now() < self.verif_to else False
