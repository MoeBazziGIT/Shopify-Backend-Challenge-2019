from django.urls import path, include
from cart import views
from rest_framework import routers

app_name = 'carts'

# these urls are here because they are not included in the router urls.
# these are function based views for doing specific actions(adding/removing products from cart, completing cart)
urlpatterns = [
    path('<int:cart_pk>/checkout/', views.cart_checkout, name='checkout'),
    path('<int:cart_pk>/add/<int:product_pk>/', views.add_item, name='add_item'),
    path('<int:cart_pk>/remove/<int:product_pk>/', views.remove_item, name='remove_item'),
]
