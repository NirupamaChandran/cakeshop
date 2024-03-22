from django.shortcuts import render,redirect
from django.views.generic import View
from shop.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from shop.models import Category,Cake,CakeVarient,Occasion,BasketItem



class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request,"register.html",{"form":form})
    

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        return render(request,"login.html",{"form":form})
    

class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Category.objects.all()
        return render(request,"index.html",{"data":qs})
    

class CakeListView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=CakeVarient.objects.filter(cakecategory=id)
        return render(request,"cake_list.html",{"data":qs})
                


class CakeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=CakeVarient.objects.get(id=id)
        return render (request,"detail.html",{"data":qs})
    

class AddToBasketView(View):
    def post(self,request,*args,**kwargs):
        occasion=request.POST.get("occasion")
        occasion_obj=Occasion.objects.get(occasion_name=occasion)
        id=kwargs.get("pk")
        cake_obj=CakeVarient.objects.get(id=id)
        BasketItem.objects.create(
           cake_varient_object=cake_obj,
           occasion_object=occasion_obj,
           basket_object=request.user.cart
        )
        return redirect("index")
    

class BasketItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        return render(request,"cart_list.html",{"data":qs})
        