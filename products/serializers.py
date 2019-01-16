
# Serializers will convert the models into json
# Each model has its own serializer

from rest_framework import serializers
from .models import Product, ProductCategory, CartProduct

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductCategory
        fields = ['title']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model  = Product
        fields = ['id', 'title', 'price', 'inventory_count', 'category']


class CartProductSerializer(serializers.Serializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model  = CartProduct
        fields = ['product']
