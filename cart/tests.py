from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Cart
from products.models import Product, ProductCategory, CartProduct
from . import views


class CartTests(APITestCase):

    '''
    Helper functions -----------------------------------------------------------
    '''

    def create_product(self, title='Random Product', price=20.00, inventory_count=5):
        url = '/products/'
        data = {'title':title, 'price':price, 'inventory_count':inventory_count}
        response = self.client.post(url, data, format='json')
        product = Product.objects.all().last()
        return product


    def create_cart(self, completed=False, total=0):
        url = '/carts/'
        data = {'completed':completed, 'total':total}
        response = self.client.post(url, data, format='json')
        cart = Cart.objects.all().last()
        return cart


    def add_product(self, product_id, cart_id):

        url = reverse('carts:add_item', kwargs={'cart_pk':cart_id, 'product_pk':product_id})
        response = self.client.get(url)

        return response


    def remove_product(self, cart_id, product_id):

        url = reverse('carts:remove_item', kwargs={'cart_pk':cart_id, 'product_pk':product_id})
        response = self.client.get(url)

        return response


    '''
    Tests ----------------------------------------------------------------------
    '''


    # 1. --------------------------ADDING PRODUCTS---------------------------------


    # this tests adding a product to a cart
    def testing_add_product_view(self):
        product = self.create_product()
        cart = self.create_cart()

        response = self.add_product(product.id, cart.id)

        # testing if the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # testing if the product added is the product that was intended to be added to the cart
        self.assertEqual(cart.products.all().first().product, product)


    def testing_adding_nonexistent_product_to_cart(self):
        cart = self.create_cart()

        # there is no product with id 1 because we havent created a product in this function.
        response = self.add_product(1, cart.id)

        # we expect to return a 404 not found if non-existent product is being added to the cart
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def testing_adding_product_to_completed_cart(self):
        product = self.create_product()
        cart = self.create_cart(completed=True, total=100)

        response = self.add_product(product.id, cart.id)

        # we expect to return a 403 FORBIDDEN if product is being added to the completed cart
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def testing_adding_product_to_nonexistent_cart(self):
        product = self.create_product()

        # there is no cart with id 1 because we havent created a cart in this function.
        response = self.add_product(product.id, 1)

        # we expect to return a 404 not found if product is being added to a non-existent cart
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def testing_adding_non_available_product(self):
        product = self.create_product(inventory_count=0)
        cart = self.create_cart()

        response = self.add_product(product.id, cart.id)

        # we expect to return a 403 FORBIDDEN if non available product is being added to the cart
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # 2. --------------------------REMOVING PRODUCTS---------------------------------


    # this tests removing product from a cart
    def testing_remove_product_view(self):
        product = self.create_product()
        cart = self.create_cart()

        self.add_product(product.id, cart.id)

        response = self.remove_product(cart.id, product.id)

        # testing if the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # testing ig the product was removed from the cart by cheking how much items are in the cart.
        # Should now be 0 because we only added 1 product to the cart
        self.assertEqual(cart.products.all().count(), 0)


    def testing_removing_non_existent_products(self):
        cart = self.create_cart()

        # there is no product with id 1 because we havent created a product in this function.
        response = self.remove_product(1, cart.id)

        # we expect to return a 404 not found if non-existent product is being removed from the cart
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def testing_removing_product_from_completed_cart(self):
        product = self.create_product()
        cart = self.create_cart(completed=True, total=100)

        response = self.remove_product(product.id, cart.id)

        # we expect to return a 403 FORBIDDEN if product is being removed from the completed cart
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def testing_removing_product_from_nonexistent_cart(self):
        product = self.create_product()

        # there is no cart with id 1 because we havent created a cart in this function.
        response = self.remove_product(product.id, 1)

        # we expect to return a 404 NOT FOUND if product is being removed from a non-existent cart
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # 3. --------------------------CHECKING OUT CARTS---------------------------------


    def testing_checking_out_cart(self):
        cart = self.create_cart()

        url = reverse('carts:checkout', kwargs={'cart_pk':cart.id})

        response = self.client.get(url)

        cart = Cart.objects.all().last()

        # testing if the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cart.completed, True)


    def testing_re_checking_out_cart(self):
        cart = self.create_cart(completed=True)

        url = reverse('carts:checkout', kwargs={'cart_pk':cart.id})

        response = self.client.get(url)

        # testing if the response is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def testing_checking_out_non_existing_cart(self):

        # cart with id 1 does not exist
        url = reverse('carts:checkout', kwargs={'cart_pk':1})

        response = self.client.get(url)

        # testing if the response is 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def testing_checking_out_cart_with_unavailable_products(self):
        product = self.create_product(inventory_count=0)
        cart = self.create_cart()

        cart_product = CartProduct(product=product)
        cart_product.save()

        cart.products.add(cart_product)

        url = reverse('carts:checkout', kwargs={'cart_pk':cart.id})

        response = self.client.get(url)

        # testing if the response is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
