from django.db import models
import json


# Each product will have a category --> /products?category=<category_title>
# will query for all products in that category
class ProductCategory(models.Model):
    title = models.CharField(max_length = 64)

    # magic method to return category title
    def __str__(self):
        return self.title


# product model
class Product(models.Model):
    title           = models.CharField(max_length = 64)
    price           = models.FloatField()
    category        = models.ForeignKey(ProductCategory,
                                        null      = True,
                                        default   = None,
                                        on_delete = models.CASCADE,)
    inventory_count = models.PositiveIntegerField()

    # magic method to return product title
    def __str__(self):
        return self.title


# CartProduct is made because when multiple quantities of the same product want to be added
# to the shopping cart, multiple instances of that product have to be added.
# Adding the same instance of a Product will not work, it'll only add one of that product
# to the cart, thats why CartProduct was made
class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self):
        return self.product.title
