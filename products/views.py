from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'public_id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__tag_name']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'balance', 'name']
    ordering = ['-price']

    def get_queryset(self):
        return Product.objects.select_related('category').defer('description')

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], url_path='set-price', permission_classes=[permissions.IsAdminUser])
    def set_custom_price(self, request):
        product = self.get_object()
        price = request.data.get('price')
        if price is None:
            return Response({'detail': 'Price is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            price = round(float(price), 2)
        except (ValueError, TypeError):
            return Response({'detail': 'Invalid price format.'}, status=status.HTTP_400_BAD_REQUEST)
        product.price = price
        product.save(update_fields=['price'])
        return Response({
            'public_id': product.public_id,
            'name': product.name,
            'price': str(product.price),
            'updated_at': timezone.now()
        }, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'tag_name'
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Category.objects.prefetch_related('products').only('id', 'tag_name')
