from django.contrib import admin
from .models import Cart_Item
# Register your models here.
class Cart_item_Admin(admin.ModelAdmin):
    readonly_fields = ['id']
admin.site.register(Cart_Item,Cart_item_Admin)