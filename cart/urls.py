from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name="cart"),
    path('add_to_cart/<int:productid>',views.add_to_cart,name="add_to_cart"),
    path('remove_from_cart/<int:productid>',views.remove_from_cart,name="remove_from_cart")
]
