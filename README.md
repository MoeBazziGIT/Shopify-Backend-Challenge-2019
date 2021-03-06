# Shopify Backend Challenge 2019
A Django REST API of the barebones of a an online marketplace used for Shopify's 2019 backend intern challenge.

## Table of Contents
**[Getting Started](#Getting-Started)** <br>
**[Interacting With The API](#Interacting-With-The-API)** <br>
**[Testing](#Testing)**

<br>
<br>

## Getting Started
**1. To get started, you must have at least python 3.6 and Pip install installed on your computer.**

**2. Clone the project onto your computer:**

```
$ git clone https://github.com/MoeBazziGIT/Shopify-Backend-Challenge-2019.git
```

**3. Create a virtual enviroment:**

  -Linux and Macos:
```
$ python3 -m venv myvenv
```

  -Windows:
```
$ python -m venv myvenv
```

**4. You can now activate the virtual environment:**

  -Linux or MacOs:
```
$ source myvenv/bin/activate
```

  -Windows:
```
$ myvenv\Scripts\activate
```

You should now see in your terminal:
```
(myvenv) user\...
```

**5. Install Django and the Django REST framework:**

```
$ pip install Django
```

```
$ pip install djangorestframework
```

-Now cd into the project

```
$ cd Shopify-Backend-Challenge-2019
```

**6. Migrate the database:**
```
$ python manage.py migrate
```

**7. Create a Super User:**

*Note: creating a SuperUser is only needed if you want to go to the admin panel and add or modify the data tables*

```
$ python manage.py createsuperuser
```
   *It will ask to create a username and password, email is not required*

**8. Now you can launch the server:**
```
$ python manage.py runserver
```
**9. Great Job! You're all set. Now let's teach you how to interact with the project.**

## Interacting With The API

This API allows you to fetch products and carts, all at once or one at a time. You can also add and remove products from the carts as well as checkout a specific cart. You can also exclusively fetch the products that are in stock and/or fetch products in a certain category ie. clothes. Let's show you how to do all this.

**1. Products**

-Each product has 5 feilds: id, title, inventory count, and category it belongs to.


-Fetching all products:
```
/products
```

-*Note: Categories are a seperate field in the database and have a One-to-Many relationship with the products, however, you cannot access the category table through the API. To see all categories, you must do so through the admin panel*

-Fetching a specific product:
```
/products/<product_id>
```

-Fetching only products that are available:
```
/products/?available=true
```

-You can also add another parameter to fetch certain categories, or you can search for categroies alone:
```
/products/?available=true&category=electronics
```

-This will give you all the availabe products under the category electronics

**2. Carts**

-Each cart has 4 fields: id, products, total, completed(boolean for whether a cart has been checked out)

-Fetching all carts:

```
/carts
```

-Fetching a specific cart:
```
/products/<cart_id>
```

-Adding a product to the cart:
```
/products/<cart_id>/add/<product_id>

```

-Removing a product from the cart:
```
/products/<cart_id>/remove/<product_id>

```

-Note: if you try to add a product with no stock to the cart, you'll get an error message


-Checkout a cart:

```
/carts/<cart_id>/checkout
```
-Note: Once a cart has been checked out, it cannot be checkout again nor have items removed or added to it.


-Fetching only carts that have been checked out:
```
/carts?completed=true
```

## Testing

- The test.py file is located under the cart directory. Testing the cart app:

```
$ python manage.py test cart
```

## Thank you!
