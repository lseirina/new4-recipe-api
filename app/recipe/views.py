"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe import serializers
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe API."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Get serializer list for view."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class