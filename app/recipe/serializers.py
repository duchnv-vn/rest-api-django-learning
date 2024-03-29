"""
Serializers for recipe API view
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from tag.serializers import TagSerializer
from ingredient.serializers import IngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for recipe object """
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link',
            'tags',
            'ingredients',
            'image',
        ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """ Get or create tags """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, is_created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """ Get or create ingredients """
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, is_created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """ Create a recipe """
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """ Update a recipe """
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """ Serializer for recipe detail object """
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


class RecipeImageSerializer(serializers.ModelSerializer):
    """ Serializer for upload image to recipe """
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {
                'required': 'True',
            }
        }
