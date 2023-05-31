from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from Cart_Order.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        exclude = ('cart',)
        
