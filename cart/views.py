from rest_framework.decorators import action
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed, ValidationError

from products.models import Product
from .models import CartItem, ShoppingCart, OrderItem
from .serializers import CartItemSerializer, ShoppingCartSerializer, OrderItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    lookup_field = 'public_id'
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter, ]
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

    @action(detail=False, methods=['post'], url_path='checkout', permission_classes=[permissions.IsAuthenticated])
    def checkout(self, request):
        user = request.user

        try:
            shopping_cart = ShoppingCart.objects.get(user=user)
        except ShoppingCart.DoesNotExist:
            return Response({"detail": "Shopping cart not found."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            cart_items = CartItem.objects.filter(shopping_cart=shopping_cart).select_related('product')
            if not cart_items.exists():
                return Response({"detail": "Your shopping cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            order_items_to_create = []

            for item in cart_items:
                try:
                    each_product = Product.objects.select_for_update().get(id=item.product.id)
                except Product.DoesNotExist:
                    raise ValidationError("Product not found.")

                if item.number > each_product.balance:
                    raise ValidationError({
                        "detail": f"Insufficient stock for product '{each_product.name}'. Current stock: {each_product.balance}"
                    })

                each_product.balance -= item.number
                each_product.save()

                order_items_to_create.append(OrderItem(
                    user=user,
                    product=each_product,
                    name=each_product.name,
                    description=each_product.description,
                    category=str(each_product.category),
                    number=item.number,
                    price=each_product.price
                ))
            OrderItem.objects.bulk_create(order_items_to_create)
            cart_items.delete()

            return Response({"detail": "Checkout successful. Stock updated and cart cleared."},
                            status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'public_id'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter, ]
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
