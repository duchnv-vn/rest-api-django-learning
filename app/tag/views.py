"""
Views for tag APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe.serializers import (
    TagSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    """ View for manage tag APIs """
    serializer_class = TagSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve tags for authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """ Create a new tag """
        return serializer.save(user=self.request.user)
