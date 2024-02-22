"""
Views for ingredient APIs
"""
from rest_framework import mixins
from core.models import Ingredient
from ingredient.serializers import IngredientSerializer
from common.views.tag_ingredient \
    import BaseAuthenticatedTagAndIngredientViewSet


class IngredientViewSet(
    BaseAuthenticatedTagAndIngredientViewSet,
    mixins.RetrieveModelMixin,
):
    """ View for manage ingredient APIs """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
