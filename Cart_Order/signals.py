from django.db.models.signals import post_save , post_init
from django.dispatch import receiver
from Product.models import ProductModel
from .models import CartItem , CartModel


@receiver(post_init,sender=ProductModel)
def check_in_stock(sender,instance,**kwargs):
    if (instance.in_stock == False) or (instance.count <= 0) :
        CartItem.objects.filter(product=instance).delete()
        
@receiver(post_init,sender=ProductModel)
def check_quantity(instance,**kwargs):
    items = CartItem.objects.filter(product=instance)
    for item in items:
        if item.quantity > instance.count:
            item.delete()