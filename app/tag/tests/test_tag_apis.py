"""
Tests for tag APIs
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
# from rest_framework import status

from core.models import Tag
from recipe.serializers import (
    TagSerializer,
)


class PublicTagApisTests(TestCase):
    """ Test for unauthenticated tag APIs """

    def setUp(self):
        self.client = APIClient()


class PrivateTagApisTests(TestCase):
    """ Test for authenticated tag APIs """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='12345678',
        )
        self.client.force_authenticate(self.user)
