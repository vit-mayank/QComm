from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from checkout.models import Checkout
from seller.models import Dark_Store
# Create your models here.

class Order_Item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField(blank=True)

    def __str__(self):
        return self.user.username+"-"+self.product.title
    def save(self,*args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args,**kwargs)

status_choices = (
    ('delivered','Delivered'),
    ('out_for_delivery','Out For Delivery'),
    ('packed','Packed'),
    ('confirmed','Confirmed'),
    ('pending','Pending')
)
def get_initial():
    return Dark_Store.objects.all().first().id
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_no = models.IntegerField(blank=True)
    total = models.IntegerField(blank = True)
    status = models.CharField(max_length=16, choices=status_choices,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_items = models.ManyToManyField(Order_Item)
    checkout = models.ForeignKey(Checkout,on_delete=models.CASCADE,null=True)
    dark_store = models.ForeignKey(Dark_Store,on_delete=models.CASCADE,default=get_initial)

    def __str__(self):
        return self.user.username+"-"+str(self.order_no)
    
    def save(self, *args, **kwargs):  
        if not self.pk:
            last_order = Order.objects.filter(user=self.user).order_by('-order_no').first()  
            self.order_no = (last_order.order_no + 1) if last_order else 1
        if not self.total:
            inst = Order_Item.objects.filter(user = self.user)
            total = 0
            for i in inst:
                total+=i.price
            self.total = total
        super().save(*args, **kwargs) 
