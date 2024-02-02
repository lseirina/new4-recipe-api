"""Test for tag api."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def create_user(email='test@example.com', password='testpass'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicTagApiTest(TestCase):
    """Test unauthenticated requests"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tags_unauthorized(self):
        """test requered authentication for retrieving tags."""
        res = self.clent.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagApiTest(TestCase):
    """Test for authenticated requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticated(self.user)

    def test_retrieve_list_success(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name='Desert')
        Tag.objects.create(user=self.user, name='Vegan')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        another_user = get_user_model().objects.create_user(
            email='user2@example.com',
            password='testpass123'
        )
        tag = Tag.objects.create(user=self.user, name='Lunch')
        Tag.objects.create(user=another_user, name='Desert')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)



