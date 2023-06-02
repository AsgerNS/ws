from django.urls import path
from .views import *

urlpatterns = [
    path('login', login),
    path('signup', signup),
    path('logout', logout),
    path('products', get_products),
    path('product', create_product),
    path('product/<int:pk>', change_product),
    path('cart', get_cart),
    path('cart/<int:pk>', post_cart),
    path('order', order),
]