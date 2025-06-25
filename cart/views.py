from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Cart_Item
from products.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def cart(request):
    cart_obj = Cart_Item.objects.filter(user=request.user)
    if cart_obj:
        items=[]
        total = 0
        for item in cart_obj:
            items+=[[item,item.product.price * item.quantity]]
            total += item.product.price * item.quantity
        ctx = {"items":items,"total":total}
        return render(request,"cart/cart_page.html",ctx)
    else:
        return render(request,"cart/cart_page.html")

@login_required
def add_to_cart(request,productid):
    inst = Cart_Item.objects.filter(user=request.user,product_id = productid).first()
    if inst:
        inst.quantity += 1
        inst.save()
    else:
        product = Product.objects.filter(pk = productid).first()
        new_inst = Cart_Item(user=request.user,product=product,quantity = 1)
        new_inst.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_from_cart(request,productid):
    inst = Cart_Item.objects.filter(user=request.user,product_id = productid).first()
    if inst:
        inst.quantity -= 1
        if inst.quantity == 0:
            inst.delete()
        else:
            inst.save()
    else:
        product = Product.objects.filter(pk = productid).first()
        new_inst = Cart_Item(user=request.user,product=product,quantity = 1)
        new_inst.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
