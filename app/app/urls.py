"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from django.conf.urls.static import static
from django.conf import settings
from core.views import health_check
from common.constant import API_ENDPOINTS

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/' + API_ENDPOINTS['health-check'],
        health_check,
        name='health-check',
    ),
    path(
        'api/' + API_ENDPOINTS['schema'],
        SpectacularAPIView.as_view(),
        name='api-schema',
    ),
    path(
        'api/' + API_ENDPOINTS['docs'],
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path(
        'api/' + API_ENDPOINTS['user']['base'],
        include('user.urls'),
    ),
    path(
        'api/' + API_ENDPOINTS['recipe']['base'],
        include('recipe.urls'),
    ),
    path(
        'api/' + API_ENDPOINTS['tag']['base'],
        include('tag.urls'),
    ),
    path(
        'api/' + API_ENDPOINTS['ingredient']['base'],
        include('ingredient.urls'),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
