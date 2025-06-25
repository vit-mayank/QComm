from django.urls import path
from . import views
urlpatterns = [
    path('',views.seller,name="seller"),
    path("dark_store/<int:darkstoreid>",views.dark_store,name="dark_store"),
    path("edit_product/<int:darkstoreid>/<int:inventoryid>",views.edit_product,name="edit_product"),
    path("create_product/<int:darkstoreid>",views.create_product, name="create_product"),
    path('delete_item/<int:darkstoreid>/<int:inventoryid>',views.delete_product,name="delete_product"),
    path('search/',views.seller_search,name="seller_search"),
    path('orders/<int:darkstoreid>',views.seller_orders,name="seller_orders"),
    path('order/<int:orderid>',views.seller_order,name="seller_order"),
]
