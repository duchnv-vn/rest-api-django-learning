"""
Test for ingredient APIs
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient
from ingredient.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('ingredient:ingredient-list')


def detail_url(ingredient_id):
    """ Create and return a ingredient detail """
    return reverse('ingredient:ingredient-detail', args=[ingredient_id])


def create_user(**params):
    """ Create and return a new user """
    defaults = {
        'email': 'user@example.com',
        'password': '12345678',
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


class PublicIngredientApisTests(TestCase):
    """ Test for unauthenticated ingredient APIs """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test auth is required to call API """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApisTest(TestCase):
    """ Test for authenticated ingredient APIs """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='12345678',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """ Test retrieve ingredients successfully """
        Ingredient.objects.create(name="Ingredient 1", user=self.user)
        Ingredient.objects.create(name="Ingredient 2", user=self.user)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_ingredients_limited_to_user(self):
        """ Test retrieve ingredients limited to authenticated user """
        other_user = create_user(
            email='other@example.com',
            password='12345678'
        )

        Ingredient.objects.create(name="Ingredient 1", user=other_user)
        Ingredient.objects.create(name="Ingredient 2", user=self.user)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredients = Ingredient.objects.filter(user=self.user)
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_a_ingredient_by_id(self):
        """ Test retrieve an ingredient by id successfully """
        ingredient = Ingredient.objects.create(
            name="Ingredient 1", user=self.user)
        url = detail_url(ingredient.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredientFromDb = Ingredient.objects.get(name=ingredient.name)
        serializer = IngredientSerializer(ingredientFromDb)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredient(self):
        """ Test update an ingredient """
        ingredient = Ingredient.objects.create(
            name="Ingredient 1", user=self.user)
        url = detail_url(ingredient.id)

        payload = {
            "name": "Updated ingredient name"
        }

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """ Test delete an ingredient """
        ingredient = Ingredient.objects.create(
            name="Ingredient 1", user=self.user)
        url = detail_url(ingredient.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())
