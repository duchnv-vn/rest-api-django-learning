"""
Serializer for ingredient API view
"""
from rest_framework import serializers
from core.models import Ingredient


class IngredientSerializer():
    """ Serializer for ingredient object """
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']
