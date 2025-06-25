from django.db import models
from django.contrib.auth.models import User
# Create your models here.
payment_choices = [
    ('cod', 'Cash on Delivery'),
    ('card', 'Credit/Debit Card'),
    ('upi', 'UPI Payment'),
    ('wallet', 'Wallet'),
]
payment_status_choices = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
]
class Checkout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.IntegerField(blank=True,null=True)
    shipping_address = models.TextField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=payment_choices)
    payment_status = models.CharField(max_length = 20 , choices = payment_status_choices, default = 'pending')

    def __str__(self):
        return self.user.username