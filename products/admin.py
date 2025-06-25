from django.contrib import admin
from .models import Product_category,Product_subcategory,Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['id',]
admin.site.register(Product,ProductAdmin)
admin.site.register(Product_category)
admin.site.register(Product_subcategory)