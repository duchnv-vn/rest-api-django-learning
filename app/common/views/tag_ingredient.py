from rest_framework import (
    mixins,
    viewsets,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT,
                enum=[0, 1],
                description='Filter by items assigned to recipes',
            ),
        ],
    ),
)
class BaseAuthenticatedTagAndIngredientViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ Base authenticated viewset for tags and ingredients """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve items for authenticated user """
        queryset = self.queryset
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
