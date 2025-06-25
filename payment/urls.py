from django.urls import path
from . import views

urlpatterns = [
    path('create_order_id/',views.create_order_id,name="create_order_id"),
    path('verify_payment/',views.verify_payment,name="verify_payment"),
]
