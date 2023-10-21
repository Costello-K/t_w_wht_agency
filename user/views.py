from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from common.pagination import get_serializer_paginate
from common.permissions import IsOwner
from team.serializers import TeamSerializer
from user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for User objects, providing CRUD operations for user management.

    Attributes:
        serializer_class: The serializer class used for user object serialization.
        ordering (tuple): The default ordering for the queryset results.
    """
    serializer_class = UserSerializer
    ordering = ('created_at', )

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        queryset = User.objects.all()

        queryset = queryset.order_by(*self.ordering)

        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticatedOrReadOnly]

        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy', 'requests']:
            permission_classes = [IsOwner]
        elif self.action in ['teams_leader', 'teams_member']:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def teams_leader(self, request, pk=None):
        """
        Retrieve teams led by the user.
        """
        if not pk or pk != request.user.id:
            raise NotFound({'message': _('Page not found.')})
        queryset = request.user.my_teams_leader.order_by(*self.ordering)
        return get_serializer_paginate(self, queryset, TeamSerializer)

    @action(detail=False, methods=['get'])
    def teams_member(self, request, pk=None):
        """
        Retrieve teams the user is a member of.
        """
        if not pk or pk != request.user.id:
            raise NotFound({'message': _('Page not found.')})
        queryset = request.user.my_teams_member.order_by(*self.ordering)
        return get_serializer_paginate(self, queryset, TeamSerializer)
