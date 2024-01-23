"""
Tests for user APIs
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class UserApisTests(TestCase):
    """ Tests for user APIs """

    def test_user_create_api(self):
        """ Test user create api works """
