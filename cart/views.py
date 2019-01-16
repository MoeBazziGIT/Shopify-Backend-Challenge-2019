from .models import Cart
from products.models import Product, CartProduct
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .serializers import CartSerializer

import json

# This is the main view for the carts that can display all carts or only carts that are
# complete(checked out) using ?completed=true in the url. The router also generates
# a detail view for each cart using --> /carts/<pk>
class CartView(viewsets.ModelViewSet):

    serializer_class = CartSerializer

    def get_queryset(self):
        completed = self.request.query_params.get('completed', None)
        # if no params in url, complete is set to None and ignored
        if completed:
            carts = Cart.objects.filter(completed=True)
        else:
            carts = Cart.objects.all()
        return carts


# function based view for adding a product to cart
@api_view()
def add_item(request, **kwargs):
    if request.method == 'GET':

        # retrive cart and product we want to add
        cart    = Cart.objects.filter(pk=kwargs.get('cart_pk')).first()
        product = Product.objects.filter(pk=kwargs.get('product_pk')).first()

        # once a cart has been already checked out, new products cannot be added to it
        if cart and cart.completed:
            response = {'Error': f'cart #{cart.pk} has already been checked out'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        # if cart exists and product has available stock
        if cart and product and product.inventory_count:

            # creating brand new instance of CartProduct extending from Product
            product_to_add = CartProduct(product = product)
            product_to_add.save()

            # adding it to the cart
            cart.products.add(product_to_add)
            cart.save()

            # adding the price of the product to the cart total
            cart.update_cart_total(product, 'add')
            cart.save()

            # return response of success message in json
            response = {'Success': f'{product.title} added to cart #{cart.pk}'}
            return Response(response)

        # if either the cart or product doesnt exist or the stock isnt available for product
        else:
            if not cart:
                response = {'Error': 'No cart with that id'}
                _status = status.HTTP_404_NOT_FOUND
            elif not product:
                response = {'Error': 'No product with that id'}
                _status = status.HTTP_404_NOT_FOUND
            else:
                response = {'Error': f'{product} is out of stock'}
                _status = status.HTTP_403_FORBIDDEN
            return Response(response, status=_status)


# function based view for removing a product from the cart
@api_view()
def remove_item(request, **kwargs):
    if request.method == 'GET':
        cart              = Cart.objects.filter(pk=kwargs.get('cart_pk')).first()
        product           = Product.objects.filter(pk=kwargs.get('product_pk')).first()

        # if cart is already checked out then removing a product from it is forbidden
        if cart and cart.completed:
            response = {'Error': f'cart #{cart.pk} has already been checked out'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        # retrieving the already created instance of CartProduct from this cart
        product_to_delete = CartProduct.objects.filter(product=product).first()

        if cart and product_to_delete:
            # removing the CartProduct instance from this cart
            cart.products.remove(product_to_delete)
            cart.save()

            # subtracting product price from cart total
            cart.update_cart_total(product, 'remove')
            cart.save()

            # deleting this CartProduct instance from databse as there is no need for it anymore
            product_to_delete.delete()

            # return response of success message in json
            response = {'Success': f'{product.title} removed from cart #{cart.pk}'}
            return Response(response)

        # if cart or product doesnt exist in this cart
        else:
            if not cart:
                response = {'Error': f'No cart with id #{kwargs.get("cart_pk")}'}
            elif not product_to_delete:
                response = {'Error': f'No product with id #{kwargs.get("product_pk")} in cart #{kwargs.get("cart_pk")}'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


# function based view for completeing/checking out cart
@api_view()
def cart_checkout(request, **kwargs):

    # retrieve cart
    cart = Cart.objects.filter(pk = kwargs.get('cart_pk')).first()

    # if the cart requested does not exist
    if not cart:
        response = {'Error': f'cart #{kwargs.get("cart_pk")} does not exist'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    # once a cart has been already checked out, it cant happen again
    if cart.completed:
        response = {'Error': f'cart #{cart.pk} has already been checked out'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    # this dictionary will keep track of each of the products inventory count so that
    # we can use the number to be displayed in the error response message later.
    # We will also use this dictionary to retrieve the correct inventory counts
    # for each product if a product in the cart runs out of inventory, because we will be
    # decrementing each product inventory_count in each loop.
    all_inventory_counts  = {}
    for item in cart.products.all():

        # if the product is not in the dictionary already, add it.
        # the key will be the products title and the value is its inventory_count
        if not item.product.title in all_inventory_counts:
            all_inventory_counts[item.product.title] = item.product.inventory_count

        # if the product ran out of inventory before this function has completed, that means
        # this cart is trying to checkout more of this product than is available
        if not item.product.inventory_count:

            # we will count how much of this product is trying to be bought and store it
            # in this product_quantity variable
            product_quantity = 0

            # looping through the carts products and counting how much of this product is in the cart.
            # This loop is also assigning back the correct inventory_count for each product
            # using the all_inventory_counts dictionary above
            found_product = False
            for thing in cart.products.all():
                # This conditional statment is checking if we have found the product
                # that has no inventory, therefore we do not need to proceed further into the cart
                if thing.product.pk != item.product.pk and found_product:
                    break
                if thing.product.pk == item.product.pk:
                    product_quantity += 1
                    found_product = True
                thing.product.inventory_count = all_inventory_counts[thing.product.title]
                thing.product.save()

            # returning error response message that the checkout process failed and why
            response = {'Error': f'only {all_inventory_counts[item.product.title]} of {item.product.title}(s) are available. To complete order, remove {product_quantity - all_inventory_counts[item.product.title]} {item.product.title}(s) from cart, then checkout again'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        # if products inventory_count is still available, decrement and continue
        item.product.inventory_count -= 1
        item.product.save()

    # cart is now complete, and cant be checked out again
    cart.completed = True
    cart.save()

    # return response of success message
    response = {'Success': f'Cart #{cart.pk} has been checked out'}
    return Response(response)
