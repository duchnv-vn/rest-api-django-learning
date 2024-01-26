"""
Serializers for tag API view
"""
from rest_framework import serializers
from core.models import Tag


class TagSerializer(serializers.Serializer):
    """ Serializer for tag object """
    class Meta:
        model = Tag
        fields = ['name']
