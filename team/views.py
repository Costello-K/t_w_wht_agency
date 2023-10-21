from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from common.pagination import get_serializer_paginate
from common.permissions import IsLeader
from team.models import Team
from user.serializers import UserSerializer

from .serializers import TeamSerializer

User = get_user_model()


class TeamViewSet(viewsets.ModelViewSet):
    """
    A viewset for Team objects, providing CRUD operations for team management.

    Attributes:
        serializer_class: The serializer class used for team object serialization.
        ordering (tuple): The default ordering for the queryset results.
    """
    serializer_class = TeamSerializer
    ordering = ('created_at', )

    def get_queryset(self):
        """
        Get the list of teams for this view.
        """
        queryset = Team.objects.all()

        queryset = queryset.order_by(*self.ordering)

        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticatedOrReadOnly]

        if self.action in ['update', 'partial_update', 'destroy', 'add_member', 'remove_member']:
            permission_classes = [IsLeader]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def members(self, request, team_pk=None):
        """
        Retrieve the list of members in a team.
        """
        queryset = Team.get_members(team_pk).order_by(*self.ordering)

        # perform serialization and apply pagination
        return get_serializer_paginate(self, queryset, UserSerializer)

    @action(detail=True, methods=['post'])
    def add_member(self, request, team_pk=None, pk=None):
        """
        Add a user as a member to the team.
        """
        team = get_object_or_404(Team, pk=team_pk)
        team.add_member(pk)

        return Response({'message': 'User added to the team.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def remove_member(self, request, team_pk=None, pk=None):
        """
        Remove a user from the team.
        """
        team = get_object_or_404(Team, pk=team_pk)
        team.remove_member(pk)

        return Response({'message': 'User removed from the team.'}, status=status.HTTP_200_OK)
