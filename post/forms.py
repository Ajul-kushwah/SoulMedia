from django import forms
from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','image']

# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=100,label='Title')
#     body = forms.CharField(max_length=200)