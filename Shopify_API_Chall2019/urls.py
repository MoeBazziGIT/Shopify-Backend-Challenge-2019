from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from products import views as product_views
from cart import views as cart_views
from rest_framework import routers

# setting up router
router = routers.DefaultRouter()

# these two routers will provide url mappings to main views of the API

# /products/ --> will get all products in the database
# /products/<product_id>/ --> will get a specific product
router.register('products', product_views.ProductView, base_name='products')

# /carts/ --> will get all carts in the database
# /carts/<cart_id>/ --> will get a specific cart
router.register('carts', cart_views.CartView, base_name='carts')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('carts/', include('cart.urls', namespace='carts'))
]

    # the reason we include cart.urls is because this app has some extra functionality with
    # the carts ex. --> carts/checkout, add, remove. These are function based views that arent
    # included with the routers above.
