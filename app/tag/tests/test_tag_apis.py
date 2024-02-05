"""
Tests for tag APIs
"""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    Tag,
    Recipe,
)
from tag.serializers import TagSerializer

TAGS_URL = reverse('tag:tag-list')


def detail_url(tag_id):
    """ Create and return a tag detail """
    return reverse('tag:tag-detail', args=[tag_id])


def create_user(**params):
    """ Create and return a new user """
    defaults = {
        'email': 'user@example.com',
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

    def test_filter_tags_assign_to_recipes(self):
        """ Test listing only tags assigned to at least 1 recipe """
        tag_1 = Tag.objects.create(
            name="Tag 1",
            user=self.user,
        )
        tag_2 = Tag.objects.create(
            name="Tag 2",
            user=self.user,
        )
        recipe = Recipe.objects.create(
            user=self.user,
            title='Recipe 1',
            time_minutes=20,
            price=Decimal('5.25'),
            description='Sample recipe description',
            link='https:/example.com/recipe.pdf',
        )
        recipe.tags.add(tag_1)

        params = {'assigned_only': 1}
        res = self.client.get(TAGS_URL, params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer_tag_1 = TagSerializer(tag_1)
        serializer_tag_2 = TagSerializer(tag_2)
        self.assertIn(serializer_tag_1.data, res.data)
        self.assertNotIn(serializer_tag_2.data, res.data)

    def test_filtered_tags_unique(self):
        """ Test filtered tags list is no duplicated """
        tag_1 = Tag.objects.create(
            name="Tag 1",
            user=self.user,
        )
        Tag.objects.create(
            name="Tag 2",
            user=self.user,
        )
        recipe_1 = Recipe.objects.create(
            user=self.user,
            title='Recipe 1',
            time_minutes=20,
            price=Decimal('5.25'),
        )
        recipe_2 = Recipe.objects.create(
            user=self.user,
            title='Recipe 2',
            time_minutes=40,
            price=Decimal('1.25'),
        )
        recipe_1.tags.add(tag_1)
        recipe_2.tags.add(tag_1)

        params = {'assigned_only': 1}
        res = self.client.get(TAGS_URL, params)

        self.assertEqual(len(res.data), 1)
