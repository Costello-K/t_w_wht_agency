from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path(
        '<int:pk>/',
        UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='user-detail',
    ),
    path('<int:pk>/teams/leader/', UserViewSet.as_view({'get': 'teams_leader'}), name='user-team-leaders'),
    path('<int:pk>/teams/member/', UserViewSet.as_view({'get': 'teams_member'}), name='user-team-members'),
]
