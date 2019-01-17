# Shopify-Backend-Challenge-2019
A Django REST API of the barebones of a an online marketplace used for Shopify's 2019 backend intern challenge.

## Getting Started
**1. To get started, you must have at least python 3.6 and Pip install installed on your computer.**

**2. Clone the project onto your computer:**

```
git clone https://github.com/MoeBazziGIT/Shopify-Backend-Challenge-2019.git
```

**3. Create a virtual enviroment:**

  -For linux and Macos:
```
python3 -m venv myvenv
```

  -For Windows:
```
python -m venv myvenv
```

**4. You can now activate the virtual environment:** 

-For Linux or MacOs:
```
source myenv/bin/activate
```

-For Windows:
```
myvenv\Scripts\activate
```

You should now see in your terminal:
```
(myvenv) user\...
```

**5. Now its time to download Django and the Django REST framework:**

-First Django:
```
pip install Django
```
-Now the Django REST
```
pip install djangorestframework
```

**6. Migrate the database:**
```
python manage.py migrate
```

**7. Create a Super User:**

*Note: creating a SuperUser is only needed if you want to go to the admin panel and add or modify the data tables*

```
python manage.py createsuperuser
```
   *It will ask to create a username and password, email is not required*

**8. Now you can launch the server:**
```
python manage.py runserver
```
**9. Great Job! You're all set. Now let's teach you how to interact with the project.**

##Interacting With The API

This API allows you to fetch products and carts, all at once or one at a time. You can also add and remove products from the carts as well as checkout a specific cart. You can only fetch the products that are in stock and/or fetch products in a certain category ie. clothes. Let's show you how to do all this.

**1.Products**
-To fetch all products:
```
../products
```
-This will display all the products in the marketplace.

-Each product has 5 feilds: id, title, inventory count, and category it belongs to.

-*Note: Categories are a seperate field in the database and have a One-to-Many relationship with the products, however, you cannot access the category table through the API. To see all categories, you must do so through the admin panel*

-The product list will look this:

![](https://github.com/MoeBazziGIT/Shopify-Backend-Challenge-2019/blob/master/READMEpics/Cart_List.png)
