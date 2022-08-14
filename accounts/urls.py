from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]