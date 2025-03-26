from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from apps.users.managers.user_manager import UserManager
from apps.utils.models import TimestampedModel


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """
    Custom User model with enhanced features
    """
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=255)
    mobile = models.CharField(_('mobile number'), max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
