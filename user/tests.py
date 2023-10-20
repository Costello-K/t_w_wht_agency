from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import UserFactory

User = get_user_model()


class UserTests(TestCase):
    """
    Tests for user functionality
    """
    def setUp(self):
        """
        Setup method executed before each test method.
        Creates an API client and several users for use in the tests.
        """
        self.client = APIClient()

        # create users in the database
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()

        # URL for accessing the API endpoint
        self.url_get_user_list = reverse('user-list')
        self.url_get_user_1 = reverse('user-detail', args=[self.user_1.id])
        self.url_get_user_2 = reverse('user-detail', args=[self.user_2.id])

        self.user_data = {
            'username': 'test_user_3',
            'first_name': 'Test_3',
            'last_name': 'User_3',
            'email': 'test_user_3@example.com',
            'password': 'test_password',
            'confirm_password': 'test_password',
        }

        self.updated_data = {
            'first_name': 'Updated name',
            'last_name': 'Updated last_name',
        }

    def test_list_users(self):
        # send a GET request
        response = self.client.get(self.url_get_user_list)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
        self.assertEqual(len(response.data['results']), User.objects.all().count())
        expected_users = [self.user_1.id, self.user_2.id]
        users_from_response = [user.get('id') for user in response.data['results']]
        self.assertEqual(sorted(users_from_response), sorted(expected_users))

    def test_create_user(self):
        # send a POST request
        response = self.client.post(reverse('user-list'), self.user_data, format='json')

        # assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username'), self.user_data.get('username'))
        self.assertEqual(response.data.get('email'), self.user_data.get('email'))

    def test_read_user(self):
        # send a GET request
        response = self.client.get(self.url_get_user_2)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), self.user_2.username)
        self.assertEqual(response.data.get('email'), self.user_2.email)

    def test_update_user_without_authentication(self):
        # send a PATCH request
        response = self.client.patch(self.url_get_user_1, self.updated_data, format='json')

        # assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_non_profile_owner(self):
        # perform authentication
        self.client.force_authenticate(user=self.user_2)

        # send a PATCH request
        response = self.client.patch(self.url_get_user_1, self.updated_data, format='json')

        # assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_profile_owner(self):
        # perform authentication
        self.client.force_authenticate(user=self.user_1)

        # send a PATCH request
        response = self.client.patch(self.url_get_user_1, self.updated_data, format='json')

        # assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), self.updated_data.get('first_name'))
        self.assertEqual(response.data.get('last_name'), self.updated_data.get('last_name'))

    def test_delete_user_without_authentication(self):
        # send a DELETE request
        response = self.client.delete(self.url_get_user_2)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(User.objects.filter(id=self.user_1.id).exists())

    def test_delete_non_profile_owner(self):
        # perform authentication
        self.client.force_authenticate(user=self.user_2)

        # send a DELETE request
        response = self.client.delete(self.url_get_user_1)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(id=self.user_1.id).exists())

    def test_delete_user_profile_owner(self):
        # perform authentication
        self.client.force_authenticate(user=self.user_2)

        # send a DELETE request
        response = self.client.delete(self.url_get_user_2)

        # assertions
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user_2.id).exists())
