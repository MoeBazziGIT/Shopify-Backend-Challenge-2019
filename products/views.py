from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
import json


# This view is used to return all products. Url argument can be passed in to return only
# products with available stock and/or products under a certain category
# The router also will create a url for viewing a specific product using this view --> /products/<pk>
class ProductView(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):

        # retrieve query set
        products = Product.objects.all()

        # if none of these parameters are passed in, the values for these values will be
        # set to an empty string, therefore will be ignored
        available = self.request.query_params.get('available', '')
        category = self.request.query_params.get('category', '')
        category_instance = ProductCategory.objects.filter(title__iexact=category).first()

        if available.lower() == 'true' and category_instance:
            products = Product.objects.exclude(inventory_count = 0).filter(category=category_instance)
        elif available.lower() == 'true':
            products = Product.objects.exclude(inventory_count = 0)
        elif category_instance:
            products = Product.objects.filter(category=category_instance)
        return products
