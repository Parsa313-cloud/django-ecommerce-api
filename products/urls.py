from django.urls import include , path

from .views import ProductViewSet , CategoryViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet , basename='categories')
urlpatterns = [
    path('api/shop/', include(router.urls)),
]