from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order

# Create your views here.
@login_required
def orders(request):
    inst = Order.objects.filter(user = request.user)
    ctx = {"orders":inst}
    return render(request,"orders/orders_page.html",ctx)

@login_required
def order_page(request,orderid):
    inst = Order.objects.filter(user=request.user, id = orderid).first()
    if inst:
        items = inst.order_items.all()
        temp=[]
        for item in items:
            temp+=[[item,item.quantity*item.price]]
        ctx = {"order":inst,"items":temp}
        return render(request,"orders/order_page.html",ctx)
    else:
        return render(request,"orders/order_page.html")

