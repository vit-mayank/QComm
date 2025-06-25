from django.shortcuts import render,redirect
from products.views import Product
from seller.models import Seller,Dark_Store,Inventory
from products.models import Product_category,Product
def main(request):
    if request.method== "POST":
        location = request.POST.get('location')
        request.session['location'] = location
        return redirect("main")
    else:
        if request.user.is_authenticated and Seller.objects.filter(user=request.user).first():
            return render(request,"seller/base.html")
        
        locations = Dark_Store.objects.all()
        categories = Product_category.objects.all()
        products_list = []
        for category in categories:
            inventory = Inventory.objects.filter(dark_store__id = request.session.get("location"), product__subcategory__category = category)
            if inventory:
                products_list += [[category,inventory]]
        return render(request,'quickcommerce/home.html',{"categories":categories,"products_list":products_list,"locations" : locations})

def search(request):
    if request.method == "GET":
        searchvalue = request.GET['searchvalue']
        all_pro = Product.objects.all()
        filtered_products =  []
        for product in all_pro:
            if searchvalue in product.title.lower() or searchvalue in product.desc.lower():
                filtered_products+=[product]
        return render(request,'products/all_products.html',{"products" : filtered_products})