"""
URL configuration for Cakebox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/",views.SignUpView.as_view(),name="register"),
    path('',views.SignInView.as_view(),name="login"),
    path("cakes/index/",views.IndexView.as_view(),name="index"),
    path("cakes/<int:pk>/list/",views.CakeListView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/detail/",views.CakeDetailView.as_view(),name="cake-detail"),
    path("cakes/<int:pk>/add_to_basket/",views.AddToBasketView.as_view(),name="add-to-basket"),
    path("cakes/basket/items/all/",views.BasketItemListView.as_view(),name="basket-items"),
    path('basket/items/<int:pk>/qty/change/',views.BasketItemUpdateView.as_view(),name="cart-qty"),
    path('basket/items/<int:pk>/remove/',views.BasketItemRemoveView.as_view(),name="basket-item-remove"),
    path('cakes/checkout/',views.CheckOutView.as_view(),name="checkout"),
    path('payment/verification/',views.PaymentVerificationView.as_view(),name="payment-verification"),
    path('orders/summary/',views.OrderSummaryView.as_view(),name="order-summary"),
    path("orders/item/<int:pk>/remove",views.OrderItemRemoveView.as_view(),name="order-item-remove"),
    path('signout/',views.SignOutView.as_view(),name="logout"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
