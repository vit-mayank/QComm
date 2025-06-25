from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
    
class Seller(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='seller_profile')
    phone = models.CharField(max_length=15,null=True,blank=True)
    
    def __str__(self):
        return self.user.username

class Dark_Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    dark_store = models.ForeignKey(Dark_Store,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Inventory(models.Model):
    dark_store = models.ForeignKey(Dark_Store,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return self.dark_store.name+"-"+self.product.title
    