from django import forms
from .models import ProductModel, SizingModel, ColorsModel


class CreateProductForm(forms.Form):
    name = forms.CharField(max_length=255, required=True,label='نام')
    description = forms.CharField(widget=forms.Textarea, required=True, max_length=500,label='توضیحات')
    price = forms.IntegerField(min_value=1000, required=True,label='قیمت')
    in_stock = forms.BooleanField(required=False,label='موجود است')
    size = forms.ModelMultipleChoiceField(SizingModel.objects.all(),label='سایزبندی')
    color = forms.ModelMultipleChoiceField(ColorsModel.objects.all(),label='رنگ ها')
    count = forms.IntegerField(min_value=1, required=True,label='تعداد موجود')
    image = forms.FileField(required=True,label='تصاویر ')
    # category = forms.ModelChoiceField(required=True)
    
class EditProductForm(forms.Form):
    name = forms.CharField(max_length=255, required=True,label='نام')
    description = forms.CharField(widget=forms.Textarea, required=True, max_length=500,label='توضیحات')
    price = forms.IntegerField(min_value=1000, required=True,label='قیمت')
    in_stock = forms.BooleanField(required=False,label='موجود است')
    size = forms.ModelMultipleChoiceField(SizingModel.objects.all(),label='سایزبندی')
    color = forms.ModelMultipleChoiceField(ColorsModel.objects.all(),label='رنگ ها')
    count = forms.IntegerField(min_value=1, required=True,label='تعداد موجود')
    image = forms.FileField(required=False,label='تصاویر ')
    