# Shopify-Backend-Challenge-2019
A Django REST API of the barebones of a an online marketplace used for Shopify's 2019 backend intern challenge.

## Getting Started
1. To get started, you must have at least python 3.6 and Pip install installed on your computer.

2. Clone the project onto your computer:

```
git clone https://github.com/MoeBazziGIT/Shopify-Backend-Challenge-2019.git
```

3. Create a virtual enviroment:

  -For linux and Macos:
```
python3 -m venv myvenv
```

  -For Windows:
```
python -m venv myvenv
```

4. You can now activate the virtual environment: 

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

5. Now its time to download Django and the Django REST framework:
First Django:
```
pip install Django
```
6. Now the Django REST
```
pip install djangorestframework
```

7. Migrate the database:
```
python manage.py migrate
```

8. Create a Super User:
*Note: creating a SuperUser is only needed if you want to go to the admin panel and add or modify the data tables*

```
python manage.py createsuperuser
```
*It will ask to create a username and password, email is not required*

9. Now you can launch the server:
```
python manage.py runserver
```
