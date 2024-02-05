"""
Views for tag APIs
"""
from tag.serializers import TagSerializer
from core.models import Tag
from common.views.tag_ingredient \
    import BaseAuthenticatedTagAndIngredientViewSet


class TagViewSet(BaseAuthenticatedTagAndIngredientViewSet):
    """ View for manage tag APIs """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
