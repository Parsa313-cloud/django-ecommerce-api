from rest_framework import serializers
from cart.models import (ShoppingCart, CartItem, OrderItem)
from products.models import Product


class ShoppingCartSerializer(serializers.HyperlinkedModelSerializer):
    cartItems = serializers.HyperlinkedRelatedField(
        view_name="cartitem-detail",
        queryset=CartItem.objects.all(),
        lookup_field="public_id",
        many=True
    )

    class Meta:
        model = ShoppingCart
        fields = ["url", "cartItems"]
        extra_kwargs = {
            'url': {'view_name': 'shoppingcart-detail', 'lookup_field': 'public_id'}
        }

class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        queryset=Product.objects.all(),
        lookup_field='public_id',
    )
    shopping_cart = serializers.HyperlinkedRelatedField(
        queryset=ShoppingCart.objects.all(),
        view_name='shoppingcart-detail',
        lookup_field='public_id',
    )
    total = serializers.ReadOnlyField(source='total')

    class Meta:
        model = CartItem
        fields = ['url', 'product', 'shopping_cart', 'number', 'total']
        extra_kwargs = {
            'url': {'view_name': 'cartitem-detail', 'lookup_field': 'public_id'}
        }


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name="product-detail",
        lookup_field="public_id",
        queryset=Product.objects.all(),
    )
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = OrderItem
        fields = ["url", 'user', 'product', 'name', 'description',
                  'category', 'number', 'price', 'time']
        extra_kwargs = {
            'url': {'view_name': 'orderitem-detail', 'lookup_field': 'public_id'}
        }
