"""
Serializers for recipe API.
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag
)

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag."""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title','time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return recipe with tags."""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=self.context['request'].user,
                name=tag['name']
        )
            recipe.tags.add(tag_obj)

        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Detail serializer for recipe."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


