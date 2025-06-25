from django.urls import path
from . import views

urlpatterns = [
    path('',views.checkout_first,name="checkout_first"),
    path('details/',views.checkout_second,name="checkout_second"),
    path('final/<int:checkout>',views.checkout_final,name="checkout_final"),
]
