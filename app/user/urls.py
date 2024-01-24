"""
URL mappings for user API
"""
from django.urls import path
from user import views
from common.constant import API_ENDPOINTS


app_name = 'user'

urlpatterns = [
    path(
        API_ENDPOINTS['user']['create'],
        views.CreateUserView.as_view(),
        name='create'
    ),
    path(
        API_ENDPOINTS['user']['token'],
        views.CreateTokenView.as_view(),
        name='token'
    ),
]
