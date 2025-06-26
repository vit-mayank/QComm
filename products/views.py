from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Product_subcategory
from seller.models import Dark_Store
from seller.models import Customer,Inventory,Seller
from django.contrib.auth.decorators import login_required

# Create your views here.
def category_products(request,categoryid):
    print(request.user.is_anonymous)
    darkstore = Dark_Store.objects.filter(pk = request.session.get('location')).first() if request.user.is_anonymous else Customer.objects.filter(user=request.user).first().dark_store
    subcategories = Product_subcategory.objects.filter(category__id = categoryid)
    products_list = []
    for subcategory in subcategories:
        inventories = Inventory.objects.filter(dark_store = darkstore,product__subcategory = subcategory)
        if inventories:
            products_list+=[[subcategory,inventories]]
    return render(request,"products/category.html",{"products_list":products_list})
    

        


    # if request.user != "AnonymousUser":
    #     print(request.user)
    #     if Seller.objects.filter(user=request.user):
    #         return redirect('main')
    #     elif request.session.get("location"):
    #         dark_store = Dark_Store.objects.filter(pk = request.session.get('location')).first()
    #         inventories = Inventory.objects.filter(dark_store = dark_store)
    #         products = []
    #         for inventory in inventories:
    #             if inventory.stock > 0:
    #                 products+=[inventory.product]
    #         ctx = {"products":products}
    #         return render(request, 'products/all_products.html',ctx)

def product_page(request,product_id):
    product = Product.objects.filter(pk = product_id)
    if product:
        product = product.first()
        print(product)
        if Inventory.objects.filter(dark_store = Customer.objects.filter(user = request.user).first().dark_store if not request.user.is_anonymous else  Dark_Store.objects.filter(pk = request.session.get('location')).first(), product=product).first():
            return render(request,'products/product_page.html',{'product':product})
    else:
        return redirect("main")