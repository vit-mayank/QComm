from django.contrib import admin
from .models import Dark_Store, Inventory,Seller,Customer
# Register your models here.
admin.site.register(Seller)
admin.site.register(Dark_Store)
admin.site.register(Inventory)
admin.site.register(Customer)