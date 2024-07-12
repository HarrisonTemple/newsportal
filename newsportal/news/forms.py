from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
