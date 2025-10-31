from rest_framework import serializers
from cart.models import (ShoppingCart)


class ShoppingCartSerializer(serializers.HyperlinkedModelSerializer):
    # cartItems=CartItemSerializer()
    # payments=PaymentSerializer()
    class Meta:
        model = ShoppingCart
        fields = ["url", "id", "user", "cartItems", "payments"]
