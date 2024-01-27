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


class IngredientViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ view for manage ingredient APIs """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve ingredients for authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-name')
