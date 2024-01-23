"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "123456"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
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
            user = get_user_model().objects.create_user(
                email=email,
                password='123456'
            )

            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test creating non-email user will raises ValueError """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
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
