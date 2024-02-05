"""
Tests for recipe APIs
"""
from decimal import Decimal
import tempfile
import os
from PIL import Image
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """ Create and return a recipe detail """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """ Create and return a recipe """
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 20,
        'price': Decimal('5.25'),
        'description': 'Sample recipe description',
        'link': 'https:/example.com/recipe.pdf'
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


def image_upload_url(recipe_id):
    """ Create and return an image upload URL """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


class PublicRecipeApisTests(TestCase):
    """ Test for unauthenticated recipe APIs """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test auth is required to call API """
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApisTests(TestCase):
    """ Test for authenticated recipe APIs """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='12345678',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """ Test retrieve recipe successfully """
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """ Test list of recipes is limited to authenticated user """
        other_user = create_user(
            email='other@example.com',
            password='12345678',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """ Test get recipe detail successfully """
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """ Test create recipe successfully """
        payload = {
            'title': 'Sample recipe title',
            'time_minutes': 20,
            'price': Decimal('5.25'),
            'description': 'Sample recipe description',
            'link': 'https:/example.com/recipe.pdf'
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """ Test partial update of a recipe """
        origin_link = 'https://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user, link=origin_link)

        payload = {
            'title': 'Updated recipe title',
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, origin_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """ Test full update of a recipe """
        recipe = create_recipe(user=self.user)

        payload = {
            'title': 'Updated recipe title',
            'link': 'https://example.com/updated-recipe.pdf',
            'description': 'Update sample description',
            'time_minutes': 15,
            'price': Decimal('1.25'),
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_return_error(self):
        """ Test change recipe user should return error """
        new_user = create_user(
            email='other@example.com',
            password='12345678',
        )
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """ Test delete a recipe successfully """
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """ Test delete another users recipe should return error """
        new_user = create_user(
            email='other@example.com',
            password='12345678',
        )
        recipe = create_recipe(user=new_user)
        url = detail_url(recipe.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """ Test create a recipe with new tags """
        payload = {
            'title': 'Sample recipe title',
            'time_minutes': 20,
            'price': Decimal('5.25'),
            'description': 'Sample recipe description',
            'link': 'https:/example.com/recipe.pdf',
            'tags': [
                {'name': 'Tag 1'},
                {'name': 'Tag 2'},
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes[0].tags.count(), 2)
        for tag in payload['tags']:
            self.assertTrue(
                recipes[0].tags
                .filter(
                    name=tag['name'],
                    user=self.user,
                ).exists()
            )

    def create_recipe_with_existing_tags(self):
        """ Test create a recipe with existing tags """
        tag_1 = Tag.objects.create(name="Tag 1", user=self.user)
        payload = {
            'title': 'Sample recipe title',
            'time_minutes': 20,
            'price': Decimal('5.25'),
            'description': 'Sample recipe description',
            'link': 'https:/example.com/recipe.pdf',
            'tags': [
                {'name': 'Tag 1'},
                {'name': 'Tag 2'},
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes[0].tags.count(), 2)
        self.assertIn(tag_1, recipes[0].tags.all())
        for tag in payload['tags']:
            self.assertTrue(
                recipes[0].tags
                .filter(
                    name=tag['name'],
                    user=self.user
                ).exists()
            )

    def test_create_tag_on_update(self):
        """ Test create tags on update recipe """
        recipe = create_recipe(user=self.user)
        payload = {
            'tags': [
                {'name': 'Tag 1'},
                {'name': 'Tag 2'},
            ]
        }

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload['tags']:
            self.assertTrue(Tag.objects.get(user=self.user, name=tag['name']))
            self.assertTrue(recipe.tags.get(name=tag['name']))

    def test_update_recipe_assign_tags(self):
        """ Test update a recipe for assigning tags """
        tag_1 = Tag.objects.create(name="Tag 1", user=self.user)
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_1)

        tag_2 = Tag.objects.create(name="Tag 2", user=self.user)
        payload = {
            'tags': [{'name': tag_2.name}]
        }

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_2, recipe.tags.all())
        self.assertNotIn(tag_1, recipe.tags.all())

    def test_clear_recipe_tags(self):
        """ Test clear all tags in a recipe """
        tag_1 = Tag.objects.create(name="Tag 1", user=self.user)
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_1)

        payload = {
            'tags': []
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredients(self):
        """ Test create recipe with new ingredients """
        payload = {
            'title': 'Sample recipe title',
            'time_minutes': 20,
            'price': Decimal('5.25'),
            'description': 'Sample recipe description',
            'link': 'https:/example.com/recipe.pdf',
            'ingredients': [
                {'name': 'Ingredient 1'},
                {'name': 'Ingredient 2'},
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes[0].ingredients.count(), 2)
        for ingredient in payload['ingredients']:
            self.assertTrue(
                recipes[0].ingredients
                .filter(
                    name=ingredient['name'],
                    user=self.user,
                )
                .exists()
            )

    def test_create_recipe_with_existing_ingredients(self):
        """ Test create recipe with existing ingredients"""
        ingredient = Ingredient.objects.create(
            name="Ingredient 1",
            user=self.user,
        )

        payload = {
            'title': 'Sample recipe title',
            'time_minutes': 20,
            'price': Decimal('5.25'),
            'description': 'Sample recipe description',
            'link': 'https:/example.com/recipe.pdf',
            'ingredients': [
                {'name': 'Ingredient 1'},
                {'name': 'Ingredient 2'},
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        self.assertEqual(recipes[0].ingredients.count(), 2)
        self.assertIn(ingredient, recipes[0].ingredients.all())
        for ingredientPayload in payload['ingredients']:
            self.assertTrue(
                recipes[0].ingredients
                .filter(
                    name=ingredientPayload['name'],
                    user=self.user,
                ).exists()
            )

    def test_create_ingredients_on_update(self):
        """ Test create ingredients on update recipe"""
        recipe = create_recipe(user=self.user)
        payload = {
            'ingredients': [
                {'name': 'Ingredient 1'},
                {'name': 'Ingredient 2'},
            ]
        }

        url = detail_url(recipe.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 2)
        for ingredient in payload['ingredients']:
            self.assertTrue(Ingredient.objects.get(
                name=ingredient['name'],
                user=self.user
            ))
            self.assertTrue(recipe.ingredients.get(name=ingredient['name']))

    def test_update_recipe_assign_ingredients(self):
        """ Test update recipe for assign ingredients"""
        ingredient_1 = Ingredient.objects.create(
            name='Ingredient 1',
            user=self.user,
        )
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient_1)

        ingredient_2 = Ingredient.objects.create(
            name='Ingredient 2', user=self.user)
        payload = {
            'ingredients': [{'name': ingredient_2.name}]
        }

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(ingredient_2, recipe.ingredients.all())
        self.assertNotIn(ingredient_1, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):
        """ Test clear all ingredients of a recipe"""
        ingredient = Ingredient.objects.create(
            name='Ingredient 1',
            user=self.user,
        )
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)

        payload = {
            'ingredients': [],
        }

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)

    def test_filter_by_tags(self):
        """ Test retrieve recipes by tags """
        recipe_1 = create_recipe(
            user=self.user,
            title='Recipe 1',
        )
        recipe_2 = create_recipe(
            user=self.user,
            title='Recipe 2',
        )
        recipe_3 = create_recipe(
            user=self.user,
            title='Recipe 3',
        )
        tag_1 = Tag.objects.create(name="Tag 1", user=self.user)
        tag_2 = Tag.objects.create(name="Tag 2", user=self.user)
        recipe_1.tags.add(tag_1)
        recipe_2.tags.add(tag_2)

        params = {
            'tags': f"{tag_1.id},{tag_2.id}",
        }
        res = self.client.get(RECIPES_URL, params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe_serializer_1 = RecipeSerializer(recipe_1)
        recipe_serializer_2 = RecipeSerializer(recipe_2)
        recipe_serializer_3 = RecipeSerializer(recipe_3)
        self.assertIn(recipe_serializer_1.data, res.data)
        self.assertIn(recipe_serializer_2.data, res.data)
        self.assertNotIn(recipe_serializer_3.data, res.data)

    def test_filter_by_ingredients(self):
        """ Test retrieve recipes by ingredients """
        recipe_1 = create_recipe(
            user=self.user,
            title='Recipe 1',
        )
        recipe_2 = create_recipe(
            user=self.user,
            title='Recipe 2',
        )
        recipe_3 = create_recipe(
            user=self.user,
            title='Recipe 3',
        )
        ingredient_1 = Ingredient.objects.create(
            name="Ingredient 1",
            user=self.user,
        )
        ingredient_2 = Ingredient.objects.create(
            name="Ingredient 2",
            user=self.user,
        )
        recipe_1.ingredients.add(ingredient_1)
        recipe_2.ingredients.add(ingredient_2)

        params = {
            'ingredients': f"{ingredient_1.id},{ingredient_2.id}",
        }
        res = self.client.get(RECIPES_URL, params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe_serializer_1 = RecipeSerializer(recipe_1)
        recipe_serializer_2 = RecipeSerializer(recipe_2)
        recipe_serializer_3 = RecipeSerializer(recipe_3)
        self.assertIn(recipe_serializer_1.data, res.data)
        self.assertIn(recipe_serializer_2.data, res.data)
        self.assertNotIn(recipe_serializer_3.data, res.data)


class ImageUploadTests(TestCase):
    """ Test for recipe image upload API """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='12345678',
        )
        self.client.force_authenticate(self.user)
        self.recipe = create_recipe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image(self):
        """ Test upload an image to a recipe """
        url = image_upload_url(self.recipe.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)

            payload = {
                'image': image_file
            }
            res = self.client.post(url, payload, format='multipart')

        self.recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """ Test upload invalid image """
        url = image_upload_url(self.recipe.id)

        payload = {
            'image': 'notanimage'
        }
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
