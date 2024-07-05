from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='posts_all'),
    path('search/', PostSearch.as_view(), name='posts_search'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('add/post', PostAddView.as_view(), name='post_add'),
    path('add/article', ArticleAddView.as_view(), name='post_add_article'),
]
