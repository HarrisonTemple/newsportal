from .models import Post
from .filters import PostFilter
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post
    ordering = '-publish_date'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 1

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
