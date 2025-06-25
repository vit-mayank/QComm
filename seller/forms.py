from django import forms
from allauth.account.forms import SignupForm
from .models import Seller,Inventory,Dark_Store,Customer
from orders.models import Order


class CustomSignupForm(SignupForm):
    user_choices = [
        ('customer',"Customer"),
        ('seller',"seller"),
    ]

    user_type = forms.ChoiceField(choices=user_choices,required=True)
    dark_store = forms.ChoiceField(choices=[(store.location,store.location) for store in Dark_Store.objects.all()],label="Closest Location:")

    def save(self,request):
        user = super().save(request)
        user_type = self.cleaned_data.get('user_type')
        dark_store = self.cleaned_data.get('dark_store')
        if user_type == 'seller':
            Seller.objects.create(user = user)
        else:
            Customer.objects.create(user = user, dark_store = Dark_Store.objects.filter(location = dark_store).first())
        return user
    
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['stock']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']