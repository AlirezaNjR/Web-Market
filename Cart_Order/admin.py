from django.contrib import admin
from .models import CartModel , CartItem , OrderModel , OrderItemModel
# Register your models here.

admin.site.register(CartItem)
admin.site.register(CartModel)
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)