from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from .models import CartItem, ShoppingCart, OrderItem
from .serializers import CartItemSerializer, ShoppingCartSerializer, OrderItemSerializer
from rest_framework.exceptions import PermissionDenied

from rest_framework.exceptions import MethodNotAllowed


# Create your views here.
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    lookup_field = 'public_id'
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter,]
    filterset_fields = ['date']
    search_fields = ['product__name', 'product__description']
    ordering_fields = ['date']
    ordering = ["-date"]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(shopping_cart__user=user).select_related('shopping_cart', 'product')

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            'PUT', detail="Update operation is not allowed on CartItems.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            'PATCH', detail="Partial update is not allowed on CartItems.")


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    lookup_field = 'public_id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ShoppingCart.objects.all()
        return ShoppingCart.objects.filter(user=user)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if user.is_staff:
            return obj
        if user != obj.user:
            raise PermissionDenied("You dont access to this shopping cart ")
        return obj

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'public_id'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter,]
    filterset_fields = ['time']
    search_fields = ['product__name', 'product__description']
    ordering_fields = ['time']
    ordering = ["-time"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return OrderItem.objects.select_related('product').all()

        return OrderItem.objects.filter(user=user).select_related('product')

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
