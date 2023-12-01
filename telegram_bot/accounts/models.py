import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import transaction


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        try:
            with transaction.atomic():
                user = self.model(username=username, **extra_fields)
                if password:
                    user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="id")
    username = models.CharField(max_length=150, unique=True, blank=True, verbose_name="имя пользователя")
    name = models.CharField(max_length=150, default="", verbose_name="имя")
    phone = models.CharField(max_length=40, blank=True, null=True, verbose_name="номер телефона")
    # password = models.CharField(max_length=128, blank=True, default="", verbose_name="пароль")
    telegram_id = models.CharField(max_length=250, verbose_name="телеграм id")
    payment_verification = models.BooleanField(default=False, verbose_name="подтверждение оплаты")

    is_employee = models.BooleanField(default=False, verbose_name="работник")
    is_active = models.BooleanField(default=True, verbose_name="активный")
    is_staff = models.BooleanField(default=False, verbose_name="персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="админ")

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',  # Измененное related_name для связи с группами
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',  # Измененное related_name для связи с разрешениями пользователя
        related_query_name='user'
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ["phone"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.id)
        return super(User, self).save(*args, **kwargs)
