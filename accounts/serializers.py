from rest_framework import serializers
from .models import Profile, User


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='email',
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = ['url', 'user', 'first_name', 'last_name', 'address',
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
        lookup_filed='public_id',
        read_only=True,
        many=True
    )

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'profile', 'orderItems']
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'email'}
        }
