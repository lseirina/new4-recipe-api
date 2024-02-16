"""Tests for ingrediennt API."""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingredient,
    Recipe,
    )
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def detail_url(ingredient_id):
    return reverse('recipe:ingredient-detail', args=[ingredient_id])

def create_user():
    """Create and return user."""
    return get_user_model().objects.create_user(
        email='test@example.com',
        password='testpass123',
    )

class PublicIngredientApiTest(TestCase):
    """Tests unauthenticated API request."""
    def SetUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatIngredientApiTest(TestCase):
    """Tests for authenticated requests."""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_list_of_ingredients(self):
        """Test retrieving list of ingredients is successful."""
        Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=self.user, name='Sugar')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""
        user2 = get_user_model().objects.create_user(
            email='user2@example.com',
            password='testpass'
        )
        ingredient = Ingredient.objects.create(user=self.user, name='Egg')
        Ingredient.objects.create(user=user2, name='Butter')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'],ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Oil')

        payload = {'name': 'Butter'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload, format='json')

        ingredient.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredients(self):
        """Test deleting ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Sugar')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_to_assigned_recipe(self):
        """Test filterirng the igredients to assigned only recipe."""
        ing1 = Ingredient.objects.create(user=self.user, name='Sugar')
        ing2 = Ingredient.objects.create(user=self.user, name='Flour')
        recipe = Recipe.objects.create(
            user = self.user,
            title ='Cake',
            time_minutes = 50,
            price = Decimal('7.90'),

        )
        recipe.ingredients.add(ing1)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': '1'})

        s1 = IngredientSerializer(ing1)
        s2 = IngredientSerializer(ing2)

        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
