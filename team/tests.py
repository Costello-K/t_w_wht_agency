from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import TeamFactory, UserFactory
from team.models import Team

User = get_user_model()


class TeamTests(TestCase):
    """
    Tests for team functionality
    """
    def setUp(self):
        """
        Setup method executed before each test method.
        Creates an API client, users and teams for use in the tests.
        """
        self.client = APIClient()

        # create users in the database
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.user_3 = UserFactory()
        self.user_4 = UserFactory()
        self.user_5 = UserFactory()
        self.user_6 = UserFactory()

        # create teams in the database
        self.team_1 = TeamFactory(leader=self.user_1, member=(self.user_2, self.user_3, self.user_4))
        self.team_2 = TeamFactory(leader=self.user_6, member=(self.user_1, self.user_3, self.user_5))

        # URL for accessing the API endpoint
        self.url_get_team_list = reverse('team-list')
        self.url_get_member_list_team_1 = reverse('team-members', args=[self.team_1.id])
        self.url_add_member_team_1 = reverse('team-add-member', args=[self.team_1.id, self.user_6.id])
        self.url_remove_member_team_1 = reverse('team-remove-member', args=[self.team_1.id, self.user_3.id])
        self.url_get_team_1 = reverse('team-detail', args=[self.team_1.id])
        self.url_get_team_2 = reverse('team-detail', args=[self.team_2.id])

        self.team_data = {
            'name': 'Team_3',
            'description': 'Description_3',
        }

        self.updated_team_data = {
            'name': 'Updated name',
            'description': 'Updated description',
        }

    def test_list_team(self):
        # send a GET request
        response = self.client.get(self.url_get_team_list)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), Team.objects.all().count())
        expected_users = [self.team_1.id, self.team_2.id]
        users_from_response = [team.get('id') for team in response.data['results']]
        self.assertEqual(sorted(users_from_response), sorted(expected_users))

    def test_team_members(self):
        response = self.client.get(self.url_get_member_list_team_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), Team.objects.get(id=self.team_1.id).member.count())
        expected_users = [self.user_2.id, self.user_3.id, self.user_4.id]
        users_from_response = [member.get('id') for member in response.data['results']]
        self.assertEqual(sorted(users_from_response), sorted(expected_users))

    def test_create_team(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(self.url_get_team_list, self.team_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), self.team_data.get('name'))
        self.assertEqual(response.data.get('description'), self.team_data.get('description'))

    def test_read_team(self):
        response = self.client.get(self.url_get_team_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.team_1.name)
        self.assertEqual(response.data.get('description'), self.team_1.description)

    def test_update_team_without_authentication(self):
        response = self.client.patch(self.url_get_team_1, self.updated_team_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_team_non_leader(self):
        self.client.force_authenticate(user=self.user_2)

        response = self.client.patch(self.url_get_team_1, self.updated_team_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_team_leader(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.patch(self.url_get_team_1, self.updated_team_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.updated_team_data.get('name'))
        self.assertEqual(response.data.get('description'), self.updated_team_data.get('description'))

    def test_add_member_without_authentication(self):
        response = self.client.post(self.url_add_member_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_member_non_leader(self):
        self.client.force_authenticate(user=self.user_2)

        response = self.client.post(self.url_add_member_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_member_leader(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(self.url_add_member_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user_6, Team.objects.get(id=self.team_1.id).member.all())

    def test_remove_member_without_authentication(self):
        response = self.client.post(self.url_remove_member_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_member_non_leader(self):
        self.client.force_authenticate(user=self.user_6)

        response = self.client.post(self.url_remove_member_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_member_leader(self):
        self.client.force_authenticate(user=self.user_2)

        response = self.client.post(self.url_remove_member_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(self.user_5, Team.objects.get(id=self.team_1.id).member.all())

    def test_delete_team_without_authentication(self):
        response = self.client.delete(self.url_get_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_leader_delete_team(self):
        self.client.force_authenticate(user=self.user_2)

        response = self.client.delete(self.url_get_team_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team_leader(self):
        self.client.force_authenticate(user=self.user_6)

        response = self.client.delete(self.url_get_team_2, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(id=self.team_2.id).exists())

    def test_leader_deletes_his_user_profile(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.delete(reverse('user-detail', args=[self.user_1.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user_1.id).exists())
        self.assertFalse(Team.objects.filter(id=self.team_1.id).exists())
