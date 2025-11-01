from rest_framework import serializers
from cart.models import (ShoppingCart, CartItem)
from products.models import Product


class ShoppingCartSerializer(serializers.HyperlinkedModelSerializer):
    # cartItems=CartItemSerializer()
    # payments=PaymentSerializer()
    class Meta:
        model = ShoppingCart
        fields = ["url", "id", "user", "cartItems", "payments"]


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
        fields = ['url' , 'product' , 'shopping_cart' , 'number', 'total']
        extra_kwargs = {
            'url' : {'view_name' : 'cartitem-detail' , 'lookup_field' : 'public_id'}
        }
