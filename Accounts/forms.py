from django import forms
from .models import CustomUserModel
from django.contrib.auth.forms import UserChangeForm , UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = UserCreationForm.Meta.fields + (
            'address','phone_number','address2','postal_code'
        ) # type: ignore

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = UserChangeForm.Meta.fields


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255,required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=255,required=True)
    email = forms.EmailField(max_length=255, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,max_length=255,required=True,)
    password2 = forms.CharField(widget=forms.PasswordInput,max_length=255,required=True)
    
class EditUserForm(forms.ModelForm):
    
    class Meta:
        model = CustomUserModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'address2',
            'postal_code',
            )
            