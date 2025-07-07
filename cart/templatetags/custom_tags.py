from django import template
from cart.models import Cart_Item
from orders.models import Order
from seller.models import Dark_Store

register = template.Library()

@register.simple_tag(takes_context=True)
def is_in_cart(context,productid):
    inst = Cart_Item.objects.filter(user = context['request'].user, product_id = productid).first()
    if inst:
        return inst
    else:
        return False
    
@register.simple_tag(takes_context=True)
def cart_count(context):
    inst = Cart_Item.objects.filter(user = context['request'].user)
    count = 0
    for item in inst:
        count += item.quantity  # Sum the quantity of each item
    return count

@register.simple_tag(takes_context=True)
def orders_count(context):
    dark_stores = Dark_Store.objects.filter(seller__user = context['request'].user)
    count = 0
    for dark_store in dark_stores:
        inst = Order.objects.filter(dark_store =dark_store,status="pending")
        for _ in inst:
            count+=1
    return count