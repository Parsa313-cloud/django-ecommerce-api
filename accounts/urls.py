from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, LoginView, ProfileView, UserViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileView, basename='profile')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
