import datetime
import django_filters
from django_filters import FilterSet
from .models import Post
from django import forms

class PostFilter(FilterSet):
    author__user_id__username = django_filters.CharFilter(field_name='author__user_id__username', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    publish_date = django_filters.DateFilter(widget=forms.SelectDateWidget(years=range(1990, 2025).__reversed__()), lookup_expr='gt')

    class Meta:
        model = Post
        fields = {
            'title',
            'author__user_id__username',
            'publish_date',
        }
