from django import forms
from .models import Post


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content',
        ]

class NewsAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content',
        ]
