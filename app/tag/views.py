"""
Views for tag APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tag.serializers import TagSerializer
from core.models import Tag
from common.views.tag_ingredient import BaseAuthenticatedTagAndIngredientViewSet


class TagViewSet(BaseAuthenticatedTagAndIngredientViewSet):
    """ View for manage tag APIs """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve tags for authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-name')
