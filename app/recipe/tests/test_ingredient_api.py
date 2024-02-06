"""Tests for ingrediennt API."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientApiTest(TestCase):
    """Tests autentification is required."""
    def SetUp(self):
        self.client = APIClient()

    def test_get_ingredients_limit_to_user(self):
        """Test retrieving ingredients limited to authentication user."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatIngredientApiTest(TestCase):
    """Tests for authenticated user."""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_list_of_ingredients(self):
        """Test retrieving list of ingredients is successful."""
        Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=self.user, name='Sugar')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

