from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import ShoppingCartViewSet

router = DefaultRouter()
router.register(r'shoppingCart', ShoppingCartViewSet, basename='shopping')

urlpatterns = [
    path('', include(router.urls))
]
