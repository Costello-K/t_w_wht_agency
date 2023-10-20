from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimestampModel


class CustomUser(AbstractUser, TimestampModel):
    """
    CustomUser class that extends the AbstractUser and TimeStampedModel.
    This class represents a custom user model with additional timestamp fields.
    """
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.username}: {self.first_name} {self.last_name}'
