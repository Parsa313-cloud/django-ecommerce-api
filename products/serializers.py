from rest_framework import serializers
from .models import Product , Category

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name='categories-detail',
        lookup_field='tag_name',
        read_only=True,
    )
    category_name = serializers.ReadOnlyField(source="category.tag_name")
    class Meta:
        model = Product
        fields = ['url', 'name', 'description', 'balance', 'price', 'category', 'category_name']
        extra_kwargs = {
            'url' : {'view_name' : 'products-detail', 'lookup_field' : 'public_id'}
        }

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        view_name='products-detail',
        lookup_field='public_id',
        many=True,
        read_only=True,
    )
    product_ids = serializers.SerializerMethodField()

    @staticmethod
    def get_product_ids(obj):
        return [p.public_id for p in obj.products.all()]
    class Meta:
        model = Category
        fields = ['url', 'tag_name', 'products', 'product_ids']
        extra_kwargs = {
            'url' : {'view_name' : 'categories-detail' , 'lookup_field' :'tag_name'}
        }