from rest_framework import serializers
from .models import Cart
from products.serializers import CartProductSerializer

class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(read_only = True,
                                 many      = True)

    class Meta:
        model  = Cart
        fields = ['id', 'completed', 'total', 'products']
