from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from common.permissions import IsOwner
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
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]
