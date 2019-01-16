from django.db import models
from products.models import CartProduct
import json

# Cart Model
class Cart(models.Model):
    # to indicate whether this cart has been checked out or not. Once a cart is checked out,
    # it cannot be checked out again.
    completed = models.BooleanField(
                              default    = False,
                              null       = True,
                              blank      = True)

    products = models.ManyToManyField(CartProduct,
                                      related_name = 'cart_products',
                                      blank   = True,
                                      default = None)

    total    = models.FloatField(blank   = True,
                                 default = 0.0)



    def __str__(self):
        return f'Cart #{self.pk}'



    def update_cart_total(self, product, action):

        # if a product is being added to the cart
        if action == 'add':
            self.total += product.price
        # if a product is being removed to the cart
        elif action == 'remove':
            self.total -= product.price
