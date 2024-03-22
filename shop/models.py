from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Flavour(models.Model):
    flavour_name=models.CharField(max_length=150,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.flavour_name
    
class Category(models.Model):
    category_name=models.CharField(max_length=150,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.category_name

    
class Occasion(models.Model):
    occasion_name=models.CharField(max_length=150,unique=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.occasion_name
    
class Cake(models.Model):
    name=models.CharField(max_length=150,unique=True)
    occasion_object=models.ManyToManyField(Occasion)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CakeVarient(models.Model):
    cake_object=models.ForeignKey(Cake,on_delete=models.CASCADE,related_name='cakeitem')
    flavour_object=models.ForeignKey(Flavour,on_delete=models.CASCADE,)
    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,name="cakecategory")
    image=models.ImageField(upload_to="cake_images",default="default.jpg",null=True,blank=True)
    shape_options=(
        ("Round","Round"),
        ("Square","Square"), 
        ("Rectangle","Rectangle"),
        ("Heart","Heart"), 
        ("Custom","Custom"), 
   )
    shape=models.CharField(max_length=150,choices=shape_options,default="custom")
    weight_options=(
        ("250gm","250gm"), 
        ("500gm","500gm"), 
        ("1kg","1kg"),  
        ("2kg","2kg"),
        ("Custom","Custom"), 

    )
    weight=models.CharField(max_length=150,choices=weight_options,default="500")
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)   

    

class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def cart_items(self):
        return self.cartitem.filter(is_order_placed=False)
    

    @property
    def cart_item_count(self):
        return self.cart_items.count()


class BasketItem(models.Model):
    cake_varient_object=models.ForeignKey(CakeVarient,on_delete=models.CASCADE,related_name="cakevarient")
    qty=models.PositiveIntegerField(default=1)
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    occasion_object=models.ForeignKey(Occasion,on_delete=models.CASCADE,null=True)
    is_order_placed=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)





def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)