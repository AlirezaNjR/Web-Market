from django import forms
from .models import PostModel

class PostCreateForm(forms.ModelForm):
    # title = forms.CharField(max_length=150,required=True)
    # description = MartorFormField()
    # cover = forms.ImageField(required=False)
    # author = forms.CharField( max_length=500, required=False)

    class Meta:
        model = PostModel
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput({'placeholder': 'امروز چگونه بود ؟'}),
        }
