
# All the urls for the products are being handled by the routers in the project urls.
# Nothing to see here, but you are welcome to stay!

from django.urls import path, include
from products import views

app_name = 'products'


urlpatterns = [
    # path('', views.ProductListView.as_view(), name='get_all_products'),
    # path('<int:pk>/', views.get_product, name='get_product'),
]
