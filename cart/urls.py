from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShoppingCartViewSet, CartItemViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'shopping-cart', ShoppingCartViewSet, basename='shoppingcart')
router.register(r'cart-item', CartItemViewSet, basename='cartitem')
router.register(r'order-item', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]
