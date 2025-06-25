from django.urls import path
from . import views

urlpatterns = [
    path("",views.orders,name='orders'),
    path("<int:orderid>/",views.order_page,name="order_page"),
]
