"""
Test for ingredient APIs
"""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from core.models import (
    Ingredient,
    Recipe,
)
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

    def test_filter_ingredients_assigned_to_recipes(self):
        """ Test listing only ingredients assigned to at least 1 recipe """
        ingredient_1 = Ingredient.objects.create(
            name="Ingredient 1",
            user=self.user,
        )
        ingredient_2 = Ingredient.objects.create(
            name="Ingredient 2",
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
        recipe.ingredients.add(ingredient_1)

        params = {'assigned_only': 1}
        res = self.client.get(INGREDIENTS_URL, params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer_ingredient_1 = IngredientSerializer(ingredient_1)
        serializer_ingredient_2 = IngredientSerializer(ingredient_2)
        self.assertIn(serializer_ingredient_1.data, res.data)
        self.assertNotIn(serializer_ingredient_2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """ Test filtered ingredients list is no duplicated """
        ingredient_1 = Ingredient.objects.create(
            name="Ingredient 1",
            user=self.user,
        )
        Ingredient.objects.create(name="Ingredient 2", user=self.user)
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
        recipe_1.ingredients.add(ingredient_1)
        recipe_2.ingredients.add(ingredient_1)

        params = {'assigned_only': 1}
        res = self.client.get(INGREDIENTS_URL, params)

        self.assertEqual(len(res.data), 1)
