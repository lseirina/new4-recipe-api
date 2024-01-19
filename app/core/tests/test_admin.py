"""
Tests for admin user.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin2example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='TestName'
        )

    def test_get_user_listed(self):
        """Test to get a list of users."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)
