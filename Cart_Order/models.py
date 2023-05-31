from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from Product.models import ProductModel, SizingModel, ColorsModel
# Create your models here.


class CartModel(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='UserCart',
    )

    class Meta:
        verbose_name = _('سبد خرید')
        verbose_name_plural = _('سبد های خرید')

    def __str__(self):
        return f'{self.user}'
    
    def clear_cart(self):
        for item in self.CartItem.all(): # type: ignore
            item.delete()
    
    def total_price(self):
        total = 0
        for item in self.CartItem.all():  # type: ignore
            total += item.product.price * item.quantity
        return total + 20000
    


class CartItem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE,related_name='C_Product')
    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name='CartItem'
    )
    size = models.ForeignKey(SizingModel, on_delete=models.CASCADE,related_name='C_Size')
    color = models.ForeignKey(ColorsModel, on_delete=models.CASCADE,related_name='C_Colors')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'ایتم سبد خرید'
        verbose_name_plural = 'آیتم های سبد خرید'

    def __str__(self):
        return f'{self.product} -> {self.cart}'

    def item_price(self):
        return self.product.price * self.quantity


#!--------------------- Order Models ---------------------
class OrderModel(models.Model):
    STATUS = (
        ('paid', 'پرداخت شده'),
        ('wait', 'در انتظار پرداخت'),
        ('cancelled', 'لغو شده'),
        ('delivered', 'تحویل داده شده'),
    )

    name = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=11, null=False, blank=False)
    email = models.EmailField(max_length=254, null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='UserOrder'
    )
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS,
        max_length=22, 
        default='wait', 
        null=False, 
        blank=False
        )
    pay_time = models.DateTimeField(null=True,blank=True)
    tracking_number = models.CharField(max_length=30, null=True, blank=False)
    address1 = models.CharField(max_length=255, null=False, blank=False)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=False, blank=False)
    total_price = models.PositiveBigIntegerField(null=False,blank=False,)
    
    class Meta:
        ordering = ['add_time']
        verbose_name = 'سفارش  '
        verbose_name_plural = 'سفارشات '
    
    def __str__(self):
        return f'{self.user}- {self.pk}'
    
    def get_total_price(self) -> int:
        total = 0
        for item in self.CartItem.all(): # type: ignore
            total += item.price
        return total

class OrderItemModel(models.Model):
    order = models.ForeignKey(
        OrderModel, 
        on_delete=models.CASCADE, 
        related_name='OrderItem',
        related_query_name='OrderItems'
        )
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.PositiveBigIntegerField(null=False, blank=False,)
    order_amount = models.PositiveIntegerField(
        null=False, 
        blank=False, 
        default=1
        )
    size = models.CharField(max_length=6, null=False, blank=False)
    color = models.CharField(max_length=20, null=False, blank=False)
    product = models.ForeignKey(
        ProductModel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=False
        )

    class Meta:
        ordering = ['order']
        verbose_name = 'آیتم سفارش  '
        verbose_name_plural = 'آیتم های سفارش '
    

    def __str__(self) -> str:
        return f'{self.name} in {self.order}'