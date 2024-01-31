"""
Views for ingredient APIs
"""
from rest_framework import (
    mixins,
    viewsets
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Ingredient
from ingredient.serializers import IngredientSerializer
from common.views.tag_ingredient import BaseAuthenticatedTagAndIngredientViewSet


class IngredientViewSet(
    BaseAuthenticatedTagAndIngredientViewSet,
    mixins.RetrieveModelMixin,
):
    """ View for manage ingredient APIs """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve ingredients for authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-name')
