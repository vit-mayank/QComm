from django.shortcuts import render,redirect,HttpResponse
from .models import Seller,Dark_Store,Inventory
from .decorators import is_seller
from orders.models import Order
from products.forms import ProductForm
from .forms import OrderForm

from .forms import InventoryForm
# Create your views here.
@is_seller
def seller(request):
    seller = Seller.objects.filter(user = request.user).first()
    dark_stores = Dark_Store.objects.filter(seller=seller)
    temp=[]
    for dark_store in dark_stores:
        inst = Order.objects.filter(dark_store =dark_store,status="pending")
        count = 0
        for _ in inst:
            count+=1
        temp+=[[dark_store,count]]
    return render(request, 'seller/dashboard.html',{"dark_stores":temp})

@is_seller
def dark_store(request,darkstoreid):
    temp = Dark_Store.objects.filter(pk = darkstoreid).first()
    if temp and temp.seller.user == request.user:
        inventory = Inventory.objects.filter(dark_store__id = darkstoreid)
        return render(request,"seller/dark_store.html",{"inventory":inventory,"darkstoreid":darkstoreid})
    return redirect('main')

@is_seller
def create_product(request,darkstoreid):
    darkstore = Dark_Store.objects.filter(pk = darkstoreid).first()
    if darkstore:
        if request.method == "POST":
            form1 = ProductForm(request.POST,request.FILES,prefix='form1')
            form2 = InventoryForm(request.POST,prefix = 'form2')
            if form1.is_valid() and form2.is_valid():
                product = form1.save()
                form2 = form2.save(commit=False)
                form2.dark_store = darkstore
                form2.product = product
                form2.save()
                return redirect('dark_store',darkstoreid = darkstoreid)
        else:
            form1 = ProductForm(prefix='form1')
            form2 = InventoryForm(prefix='form2')
            return render(request,'seller/create_product.html',{"form1":form1,"form2":form2})
    else:
        return redirect('main')
        

@is_seller
def edit_product(request,darkstoreid,inventoryid):
    inventory = Inventory.objects.filter(pk = inventoryid,dark_store__id = darkstoreid).first()
    if request.method == "POST":
        form1 = ProductForm(request.POST,instance=inventory.product,prefix='form1')
        form2 = InventoryForm(request.POST,instance = inventory,prefix='form2')
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2 = form2.save(commit=False)
            form2.dark_store_id = Dark_Store.objects.filter(pk = darkstoreid).first().id
            form2.product = Inventory.objects.filter(pk = inventoryid).first().product
            form2.save()
            return redirect('dark_store',darkstoreid = darkstoreid)
    temp = Dark_Store.objects.filter(pk = darkstoreid).first()
    if temp and temp.seller.user == request.user:
        if inventory:
            form1 = ProductForm(instance = inventory.product,prefix='form1')
            form2 = InventoryForm(instance=inventory,prefix='form2')
            return render(request,"seller/edit_product.html",{"form1":form1,"form2":form2})
    return redirect('main')


@is_seller
def delete_product(request,darkstoreid,inventoryid):
    inventory =  Inventory.objects.filter(pk = inventoryid,dark_store__id = darkstoreid).first()
    if inventory:
        if request.method == "POST":
            product = inventory.product
            product.delete()
            inventory.delete()
            return redirect('dark_store', darkstoreid = darkstoreid)
        return render(request,'seller/delete_product.html',{"inventory":inventory})
    return redirect('main')

@is_seller
def seller_search(request):
    if request.method == "GET":
        search_value = request.GET['searchvalue']
        dark_stores = Dark_Store.objects.filter(seller__user=request.user)
        filtered_darkstores = []
        for dark_store in dark_stores:
            if search_value in dark_store.name.lower() or search_value in dark_store.location.lower():
                filtered_darkstores += [dark_store]
        return render(request,'seller/dashboard.html',{"dark_stores":filtered_darkstores})

@is_seller
def seller_orders(request,darkstoreid):
    dark_store = Dark_Store.objects.filter(pk = darkstoreid).first()
    if dark_store:
        orders = Order.objects.filter(dark_store=dark_store)
        return render(request,"seller/orders_page.html",{"orders":orders})
    else:
        return redirect('main')

@is_seller
def seller_order(request,orderid):
    inst = Order.objects.filter(pk = orderid).first()
    if inst and inst.dark_store in Dark_Store.objects.filter(seller__user=request.user):
        if request.method=="POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                inst.status = status
                inst.save()
                return redirect('seller_orders',darkstoreid = inst.dark_store.id)
        else:
            order_items = inst.order_items.all()
            temp = []
            for order_item in order_items:
                temp+=[[order_item,order_item.price*order_item.quantity]]
            form = OrderForm(instance=inst)
            return render(request,"seller/order_page.html",{"order":inst,'order_items':temp,"form":form})
    else:
        return redirect('main')