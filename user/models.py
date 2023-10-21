from functools import partial

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimestampModel
from services.get_file_path import get_path_with_unique_filename


class CustomUser(AbstractUser, TimestampModel):
    """
    CustomUser class that extends the AbstractUser and TimeStampedModel.
    This class represents a custom user model with additional timestamp fields.
    Attributes:
        email (EmailField): An email field for user.
        avatar (ImageField): An image field for user avatars.
            - 'upload_to' specifies the upload path using a custom filename generator function.
            - 'blank=True' allows the field to be optional.
    """
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(
        _('avatar'),
        upload_to=partial(get_path_with_unique_filename, file_path='images/users/avatars'),
        blank=True,
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{self.username}: {self.first_name} {self.last_name}'

    @property
    def my_teams_leader(self):
        return self.teams_leader.all()

    @property
    def my_teams_member(self):
        return self.teams_member.all()
