from django.shortcuts import get_object_or_404
from rest_framework import permissions

from team.models import Team


class IsOwner(permissions.BasePermission):
    """
    Grants access only to the instance owner
    """
    def has_object_permission(self, request, view, instance):
        return instance == request.user


class IsLeader(permissions.BasePermission):
    """
    Grants access only to the instance leader
    """
    def has_permission(self, request, view):
        if view.action in ['add_member', 'remove_member']:
            team_pk = request.parser_context.get('kwargs', {}).get('team_pk')

            if team_pk is None:
                return False

            team = get_object_or_404(Team, pk=team_pk)
            return team.is_leader(request.user)

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, instance):
        return instance.is_leader(request.user)
