"""
Tests for tag APIs
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from tag.serializers import TagSerializer

TAGS_URL = reverse('tag:tag-list')


def detail_url(tag_id):
    """ Create and return a tag detail """
    return reverse('tag:tag-detail', args=[tag_id])


def create_user(**params):
    """ Create and return a new user """
    defaults = {
        'email': 'other@example.com',
        'password': '12345678',
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


class PublicTagApisTests(TestCase):
    """ Test for unauthenticated tag APIs """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test auth is required to call API """
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApisTests(TestCase):
    """ Test for authenticated tag APIs """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='12345678',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ Test retrieve tags successfully """
        Tag.objects.create(name="Tag 1", user=self.user)
        Tag.objects.create(name="Tag 2", user=self.user)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Test retrieve tags limited to authenticated user """
        other_user = create_user(
            email='other@example.com',
            password='12345678'
        )

        Tag.objects.create(name="Tag 1", user=other_user)
        Tag.objects.create(name="Tag 2", user=self.user)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tags = Tag.objects.filter(user=self.user)
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        """ Test update a tag """
        tag = Tag.objects.create(name="Tag 1", user=self.user)

        payload = {
            'name': 'Updated tag 1',
        }
        url = detail_url(tag.id)
        self.client.patch(url, payload)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """ Test delete a tag """
        tag = Tag.objects.create(name="Tag 1", user=self.user)

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())
