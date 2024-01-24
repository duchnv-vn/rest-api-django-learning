"""
Tests for user APIs
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUserApisTests(TestCase):
    """ Tests for public user APIs """

    def setUp(self):
        self.client = APIClient()

    def test_user_create_success(self):
        """ Test create user successful """
        payload = {
            'email': 'test@wxample.com',
            'password': '12345678',
            'name': 'Test User'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test error returned if user with email exists """
        payload = {
            'email': 'test@wxample.com',
            'password': '12345678',
            'name': 'Test User'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test error returned if password less than 5 chars """
        payload = {
            'email': 'test@wxample.com',
            'password': '1234',
            'name': 'Test User'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test create token for valid credentials """
        user_details = {
            'email': 'test@wxample.com',
            'password': '1234',
            'name': 'Test User'
        }
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        create_user(**user_details)
        print('TOKEN_URL', TOKEN_URL)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_bad_request(self):
        """ Test create token with invalid credentials """
        user_details = {
            'email': 'test@wxample.com',
            'password': '1234',
            'name': 'Test User'
        }
        payload = {
            'email': user_details['email'],
            'password': '5678',
        }

        create_user(**user_details)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """ Test create token with blank password """
        payload = {
            'email': 'test@wxample.com',
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
