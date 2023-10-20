from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Grants access only to the instance owner
    """
    def has_object_permission(self, request, view, instance):
        return instance == request.user
