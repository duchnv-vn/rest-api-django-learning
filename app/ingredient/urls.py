"""
URL mapping for ingredient APIs
"""

from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter
from ingredient import views

router = DefaultRouter()
router.register('', views.IngredientViewSet)

app_name = 'ingredient'

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
]
