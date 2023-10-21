from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from common.models import TimestampModel

User = get_user_model()


class Team(TimestampModel):
    """
    Team class that extends the TimeStampedModel.
    This class represents a team model with additional timestamp fields.
    """
    leader = models.ForeignKey(User, verbose_name=_('leader'), on_delete=models.CASCADE, related_name='teams_leader')
    # we accept that one member can be present in several teams
    member = models.ManyToManyField(User, verbose_name=_('member'), related_name='teams_member')
    name = models.CharField(_('name'), max_length=254, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def __str__(self):
        return f'id_{self.id}: {self.name[:50]}'

    @classmethod
    def get_members(cls, team_id):
        team = get_object_or_404(cls, id=team_id)
        return team.member.all()

    def is_leader(self, user):
        return self.leader == user

    def add_member(self, member_id):
        if self.member.filter(id=member_id).exists():
            raise ValidationError({'message': 'The user is already a member of the team.'})
        if member_id == self.leader.id:
            raise ValidationError({'message': 'The team leader cannot be a member.'})
        self.member.add(member_id)

    def remove_member(self, member_id):
        if not self.member.filter(id=member_id).exists():
            raise ValidationError({'message': 'The user is not a team member.'})
        self.member.remove(member_id)
