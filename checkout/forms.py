from django import forms
from .models import Checkout

class checkout_form(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['shipping_address','phone','payment_method']
