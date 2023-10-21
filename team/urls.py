from django.urls import path

from .views import TeamViewSet

urlpatterns = [
    path('', TeamViewSet.as_view({'get': 'list', 'post': 'create'}), name='team-list'),
    path(
        '<int:pk>/',
        TeamViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='team-detail'
    ),
    path('<int:team_pk>/members/', TeamViewSet.as_view({'get': 'members'}), name='team-members'),
    path('<int:team_pk>/add_member/<int:pk>/', TeamViewSet.as_view({'post': 'add_member'}), name='team-add-member'),
    path(
        '<int:team_pk>/remove_member/<int:pk>/',
        TeamViewSet.as_view({'post': 'remove_member'}),
        name='team-remove-member'
    ),
]
