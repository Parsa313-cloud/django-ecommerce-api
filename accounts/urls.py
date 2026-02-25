from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import SignUpView, ProfileView, UserViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileView, basename='profile')
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('auth/signup', SignUpView.as_view()),
    path('', include(router.urls))
]
