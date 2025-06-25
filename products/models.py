from django.db import models
from django.shortcuts import get_object_or_404
# Create your models here.
class Product_category(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to="category_images",null=True)

    def __str__(self):
        return self.title
    
class Product_subcategory(models.Model):
    category = models.ForeignKey(Product_category,on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    def __str__(self):
        return self.title
    
def get_default_subcategory():
    return get_object_or_404(Product_subcategory,title = "Others").id

class Product(models.Model):
    subcategory = models.ForeignKey(Product_subcategory, on_delete=models.SET_DEFAULT, default=get_default_subcategory)
    title = models.CharField(max_length=1000)
    desc = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="product_images",null=True)
    def __str__(self):
        return self.title
    