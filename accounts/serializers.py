from rest_framework import serializers
from .models import Profile, User
from cart.models import ShoppingCart


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True,
    )

    user_name = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Profile
        fields = ['url', "user_name", 'user', 'first_name', 'last_name', 'address',
                  'phone_number', 'slug', 'created_at', 'updated_at']
        extra_kwargs = {
            'url': {'view_name': 'profile-detail', 'lookup_field': 'slug'}
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        lookup_field='slug',
        read_only=True
    )
    orderItems = serializers.HyperlinkedRelatedField(
        view_name="orderitem-detail",
        lookup_field='public_id',
        read_only=True,
        many=True
    )
    shopping_cart = serializers.HyperlinkedRelatedField(
        view_name="shopping-detail",
        lookup_field='public_id',
        queryset=ShoppingCart.objects.all()
    )

    class Meta:
        model = User
        fields = ['url', 'username', 'email',
                  'profile', 'shopping_cart', 'orderItems']
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'username'}
        }


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
