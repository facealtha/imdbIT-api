
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet, FavoriteViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('movies', MovieViewSet)
router.register('favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]