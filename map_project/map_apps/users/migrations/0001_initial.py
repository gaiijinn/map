# Generated by Django 3.2.16 on 2024-07-14 22:37

import uuid

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import map_apps.users.models
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Електронна адреса')),
                ('is_org', models.BooleanField(db_index=True, default=False, verbose_name='Зареєстрований як організація')),
                ('is_verif', models.BooleanField(default=False, verbose_name='Верифікований')),
                ('rating', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Рейтинг')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Користувача',
                'verbose_name_plural': 'Користувачі',
            },
            managers=[
                ('objects', map_apps.users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=128)),
                ('low_range', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('top_range', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Тип рівня користувача',
                'verbose_name_plural': 'Рівні користувачів',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to='users/profile_picture/', verbose_name='Фото користувача')),
                ('about_me', models.CharField(blank=True, max_length=512, null=True, verbose_name='Про себе')),
                ('inst_link', models.URLField(blank=True, max_length=256, null=True, verbose_name='Instagram посилання')),
                ('want_newsletters', models.BooleanField(default=False, verbose_name='Згоден отримувати новини')),
            ],
        ),
        migrations.CreateModel(
            name='UserVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(default=uuid.uuid4, verbose_name='Код')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('expired_at', models.DateTimeField(blank=True, null=True, verbose_name='Дійсний до')),
                ('verif_to', models.DateTimeField(blank=True, null=True, verbose_name='Активовано до')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userverification', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_users', to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_subscriptions', to='users.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscriptions',
            field=models.ManyToManyField(through='users.UserSubscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL, verbose_name='Користувач'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userlevel', verbose_name='Рівень користувача'),
        ),
        migrations.CreateModel(
            name='HistoricalUserProfile',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('profile_picture', models.TextField(blank=True, max_length=100, verbose_name='Фото користувача')),
                ('about_me', models.CharField(blank=True, max_length=512, null=True, verbose_name='Про себе')),
                ('inst_link', models.URLField(blank=True, max_length=256, null=True, verbose_name='Instagram посилання')),
                ('want_newsletters', models.BooleanField(default=False, verbose_name='Згоден отримувати новини')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
                ('user_level', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.userlevel', verbose_name='Рівень користувача')),
            ],
            options={
                'verbose_name': 'historical user profile',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
