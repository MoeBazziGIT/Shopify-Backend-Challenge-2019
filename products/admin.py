from django.contrib import admin
from .models import Product, ProductCategory, CartProduct

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(CartProduct)
