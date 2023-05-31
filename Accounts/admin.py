from django.contrib import admin
from .models import CustomUserModel
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm , CustomUserCreationForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    add_form = CustomUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('phone_number','address','address2','postal_code')},),
    )
    
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('phone_number','address','address2','postal_code')},),
    ) # type: ignore
    
admin.site.register(CustomUserModel,CustomUserAdmin)