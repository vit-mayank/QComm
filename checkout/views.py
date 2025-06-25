from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart_Item
from .forms import checkout_form
from cart.models import Cart_Item
from orders.models import Order_Item,Order
from .models import Checkout
from seller.models import Customer
from django.conf import settings
# Create your views here.

@login_required
def checkout_first(request):
    if request.method=="POST":
        items = request.POST.items
        total = request.POST.total
        return render(request,"checkout/checkout_second.html")
    inst = Cart_Item.objects.filter(user=request.user)
    if inst:
        items=[]
        total = 0
        for item in inst:
            items+=[[item,item.product.price * item.quantity]]
            total += item.product.price * item.quantity
        ctx = {"items":items, "total":total}
        return render(request,"checkout/checkout_first.html",ctx)
    return render(request,"checkout/checkout_first.html")

@login_required
def checkout_second(request):
    inst = Cart_Item.objects.filter(user=request.user)
    if inst:
        items=[]
        total = 0
        for item in inst:
            items+=[[item,item.product.price * item.quantity]]
            total += item.product.price * item.quantity
        if request.method == "POST":
            inst = checkout_form(request.POST)
            if inst.is_valid():
                inst = inst.save(commit=False)
                inst.total = total
                inst.user = request.user
                inst.save()
                if inst.payment_method != "cod":
                    return render(request,'payment/payment.html',{"razorpay_key": settings.RAZORPAY_KEY_ID})
                return redirect('checkout_final',checkout = inst.id)
        else:
            inst = checkout_form()
            return render(request,"checkout/checkout_second.html",{"form":inst,"items":items,"total":total})
    else:
        return render(request,"base.html")

@login_required   
def checkout_final(request,checkout):
    inst = Cart_Item.objects.filter(user=request.user)
    items=[]
    total = 0
    for item in inst:
        items+=[[item,item.product.price * item.quantity]]
        total += item.product.price * item.quantity
    shipping_details = Checkout.objects.filter(pk=checkout).first()
    if request.method=="POST":
        order = Order()
        order.user = request.user
        order.total = total
        order.status = 'pending'
        order.checkout = shipping_details
        order.dark_store = Customer.objects.filter(user=request.user).first().dark_store
        order.save()
        for item in inst:
            order_item = Order_Item()
            order_item.user = request.user
            order_item.product = item.product
            order_item.quantity = item.quantity
            order_item.price = item.product.price
            order_item.save()
            item.delete()
            order.order_items.add(order_item)
        return redirect('order_page',orderid = order.id)
    return render(request,"checkout/checkout_final.html",{"items":items,"total":total,"shipping_details":shipping_details})