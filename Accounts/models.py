from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUserModel(AbstractUser):
    address = models.CharField(max_length=500,null=True ,blank=False,verbose_name='ادرس اصلی')
    address2 = models.CharField(max_length=500,null=True ,blank=False,verbose_name='ادرس دوم')
    phone_number = models.CharField(verbose_name='شماره تلفن ',max_length=11,null=True,blank=True)
    postal_code  = models.CharField(max_length=20,null=True,blank=False,verbose_name='کد پستی')
    
    def cart(self):
        return self.UserCart.first() # type: ignore
    
    def cart_item(self):
        return self.UserCart.first().CartItem.all() # type: ignore
    
    