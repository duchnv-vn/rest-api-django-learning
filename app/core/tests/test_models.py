"""
Tests for models
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from core import models


def create_user(**params):
    payload = {
        'email': 'test@example.com',
        'password': '12345678'
    }
    payload.update(params)
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "123456"
        user = create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """ Test email is normalized for new users """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = create_user(
                email=email,
                password='123456'
            )

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test creating non-email user will raises ValueError """
        with self.assertRaises(ValueError):
            create_user(
                email='',
                password='123456'
            )

    def test_create_superuser(self):
        """ Test creating superuser """
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='123456'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """ Test create a recipe successfully """
        user = create_user(
            email="test@example.com",
            password="123456"
        )

        recipe = Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """ Test create a tag successfully """
        user = create_user(
            email="test@example.com",
            password="123456"
        )

        tag = Tag.objects.create(
            name="Sample tag 1",
            user=user,
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """ Test create a ingredient successfully """
        user = create_user(
            email="test@example.com",
            password="123456"
        )

        ingredient = Ingredient.objects.create(
            name="Ingredient 1",
            user=user,
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """ Test generate image path """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
