import razorpay

from django.shortcuts import render,redirect
from django.views.generic import View
from shop.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib import messages

from shop.decorators import signin_required,owner_permission_required
from shop.models import Category,Cake,CakeVarient,Occasion,BasketItem,Order,OrderItems


KEY_ID="rzp_test_qEfodDQFfhXaCq"
KEY_SECRET="42J5m041xFFF9T14x7bgIqB2"


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
    


@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Category.objects.all()
        return render(request,"index.html",{"data":qs})
    

@method_decorator([signin_required,never_cache],name="dispatch")
class CakeListView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=CakeVarient.objects.filter(cakecategory=id)
        return render(request,"cake_list.html",{"data":qs})
                


@method_decorator([signin_required,never_cache],name="dispatch")
class CakeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")#cake_id
        qs=CakeVarient.objects.get(id=id)
        return render (request,"detail.html",{"data":qs})
    

@method_decorator([signin_required,never_cache],name="dispatch")
class AddToBasketView(View):
    def post(self,request,*args,**kwargs):
        occasion=request.POST.get("occasion")
        occasion_obj=Occasion.objects.get(occasion_name=occasion)
        qty=request.POST.get("qty")
        id=kwargs.get("pk")
        cake_obj=CakeVarient.objects.get(id=id)
        BasketItem.objects.create(
           cake_varient_object=cake_obj,
           qty=qty,
           occasion_object=occasion_obj,
           basket_object=request.user.cart
        )
        return redirect("index")
    

@method_decorator([signin_required,never_cache],name="dispatch")
class BasketItemListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        return render(request,"cart_list.html",{"data":qs})
    

@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")
class BasketItemUpdateView(View):
    def post(self,request,*args,**kwargs):
        action=request.POST.get("counterbutton")
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        if action=="+":
            basket_item_object.qty+=1
            basket_item_object.save()
        else:
            basket_item_object.qty-=1
            basket_item_object.save()
        return redirect("basket-items")
    

@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")
class BasketItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        BasketItem.objects.get(id=id).delete()
        return redirect("basket-items")
    

@method_decorator([signin_required,never_cache],name="dispatch")
class CheckOutView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        name=request.POST.get("name")
        customization=request.POST.get("customization")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        payment_method=request.POST.get("payment")

        order_obj=Order.objects.create(
            user_object=request.user,
            name=name,
            customization=customization,
            delivery_address=address,
            email=email,
            phone=phone,
            total=request.user.cart.basket_total,
            payment=payment_method
        )

        try:
            basket_items=request.user.cart.cart_items
            for bi in basket_items:
                OrderItems.objects.create(
                    order_object=order_obj,
                    basket_item_object=bi
                )
                bi.is_order_placed=True
                bi.save()
        except:
            order_obj.delete()
        finally:
            if payment_method=="online" and order_obj:
                client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
                data={"amount":order_obj.get_order_total*100,"currency": "INR", "receipt": "order_rcptid_11" }
                payment = client.order.create(data=data)
                order_obj.order_id=payment.get("id")
                order_obj.save()
                context={
                    "key":KEY_ID,
                    "order_id":payment.get("id"),
                    "amount":payment.get("amount")
                }
                return render(request,"payment.html",{"context":context})
            else:
                order_obj.save()
                return redirect("index")
            return redirect("index")


@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):
    def post(self,request,*args,**kwargs):
        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
        data=request.POST
        try:
            client.utility.verify_payment_signature(data)
            order_obj=Order.objects.get(order_id=data.get("razorpay_order_id"))
            order_obj.is_paid=+True
            order_obj.save()
            print("*************Transaction Completed******************")
        except:
            print("!!!!!!!!!!!!!!!!!Transaction Failed!!!!!!!!!!!!!!!!!!!!!")
        return render(request,"success.html")
    


class OrderSummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=Order.objects.filter(user_object=request.user).exclude(status="cancelled")
        return render(request,"order_summary.html",{"data":qs})
    

class OrderItemRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        OrderItems.objects.get(id=id).delete()
        return redirect("order-summary")


@method_decorator([signin_required,never_cache],name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")
    