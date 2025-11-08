from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets , permissions , filters

from .models import CartItem
from .serializers import CartItemSerializer

from rest_framework.exceptions import MethodNotAllowed


# Create your views here.
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    lookup_field = 'public_id'
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,]
    filterset_fields = ['date']
    search_fields = ['product__name' , 'product__description']
    ordering_fields = ['date']
    ordering = ["-date"]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(shopping_cart__user=user).select_related('shopping_cart', 'product')

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT', detail="Update operation is not allowed on CartItems.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH', detail="Partial update is not allowed on CartItems.")