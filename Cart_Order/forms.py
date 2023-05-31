from django import forms

class OrderInfoForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    family = forms.CharField(max_length=50, required=True)
    address1 = forms.CharField(max_length=500, required=True)
    address2 = forms.CharField(max_length=500, required=False)
    phone = forms.CharField(max_length=11, required=True)
    postal_code = forms.CharField( max_length=20, required=True)
    email = forms.EmailField(max_length=255,required=True)
    