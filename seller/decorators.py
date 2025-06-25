from functools import wraps
from django.shortcuts import redirect
from .models import Seller
from django.contrib.auth.decorators import login_required
def is_seller(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request,*args,**kwargs):
        seller =Seller.objects.filter(user=request.user).first()
        if not seller:
            return redirect('main')
        
        return view_func(request,*args,**kwargs)
    return _wrapped_view


