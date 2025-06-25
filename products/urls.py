from django.urls import path
from . import views

urlpatterns = [
    # path("",views.all_products,name="products"),
    path("<int:product_id>/pid/",views.product_page,name="product_page"),
    path("category/<int:categoryid>/",views.category_products,name="category_page"),
]
