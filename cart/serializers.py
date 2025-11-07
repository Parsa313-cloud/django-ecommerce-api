from rest_framework import serializers
from cart.models import ShoppingCart, CartItem, OrderItem
from products.models import Product

class ShoppingCartSerializer(serializers.HyperlinkedModelSerializer):

    cartItems = serializers.HyperlinkedRelatedField(
        view_name='cartitem-detail',
        lookup_field='public_id',
        read_only=True,
        many=True
    )

    class Meta:
        model = ShoppingCart
        fields = ['url', 'cartItems']
        extra_kwargs = {
            'url': {'view_name': 'shoppingcart-detail', 'lookup_field': 'public_id'}
        }

class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        lookup_field='public_id',
        queryset=Product.objects.all(),
    )


    shopping_cart = serializers.HyperlinkedRelatedField(
        view_name='shoppingcart-detail',
        lookup_field='public_id',
        read_only=True
    )

    total = serializers.ReadOnlyField(source='total')

    class Meta:
        model = CartItem
        fields = ['url', 'product', 'shopping_cart', 'number', 'total']
        extra_kwargs = {
            'url': {'view_name': 'cartitem-detail', 'lookup_field': 'public_id'}
        }

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        shopping_cart, _ = ShoppingCart.objects.get_or_create(user=user)
        validated_data['shopping_cart'] = shopping_cart
        return super().create(validated_data)

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):

    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        lookup_field='public_id',
        read_only=True
    )
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = OrderItem
        fields = [
            'url', 'user', 'product', 'name', 'description',
            'category', 'number', 'price', 'time'
        ]
        extra_kwargs = {
            'url': {'view_name': 'orderitem-detail', 'lookup_field': 'public_id'}
        }
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
