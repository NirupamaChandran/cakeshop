from django.shortcuts import redirect
from shop.models import BasketItem
from django.contrib import messages

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


def owner_permission_required(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item=BasketItem.objects.get(id=id)
        if basket_item.basket_object.owner != request.user:
            messages.error(request,"permission denied")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper