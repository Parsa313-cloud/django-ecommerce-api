from rest_framework import serializers
from .models import Product , Category

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='category-detail',
        lookup_field='tag_name',
    )
    class Meta:
        model = Product
        fields = ['url', 'name', 'description', 'balance', 'price', 'category']
        extra_kwargs = {
            'url' : {'view_name' : 'product-detail', 'lookup_field' : 'public_id'}
        }

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        lookup_field='public_id',
        many=True,
        read_only=True,
    )
    class Meta:
        model = Category
        fields = ['url', 'tag_name', 'products']
        extra_kwargs = {
            'url' : {'view_name' : 'category-detail' , 'lookup_field' :'tag_name'}
        }