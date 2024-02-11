"""
Tests for models.
"""
from unittest.mock import patch
import uuid

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='test@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)

class ModelTests(TestCase):

    def test_create_user_model_with_email(self):
        """Test creating user model with email is success."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normolized(self):
        """Test a new user email is normolized."""
        email_samples = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['test3@example.COM', 'test3@example.com']
        ]
        for email, expected in email_samples:
            user = get_user_model().objects.create_user(email=email, password='test123')
            self.assertEqual(user.email, expected)

    def test_raise_error_new_user_without_email(self):
        """ValueError raises if a user does not have a email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        """Test creating super user success."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        """Test create recipe is successful."""
        user = create_user()
        recipe = models.Recipe.objects.create(
            user=user,
            title='Cake',
            time_minutes=50,
            price=Decimal('10.50'),
            description='It is very tasty cake.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredients(self):
        """Test creating ingredients is successful."""
        user = create_user()
        ing = models.Ingredient.objects.create(
            user=user,
            name='Flour',
        )

        self.assertEqual(str(ing), ing.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')