from django import forms
from .models import BlogCommentModel

class BlogCommentForm(forms.ModelForm):
    
    class Meta:
        model = BlogCommentModel
        exclude = ('post',)