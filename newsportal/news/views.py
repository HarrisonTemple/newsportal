from .models import Post
from .filters import PostFilter
from .forms import PostAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class PostList(ListView):
    model = Post
    ordering = '-publish_date'
    template_name = 'posts_all.html'
    context_object_name = 'posts'
    paginate_by = 1

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    template_name = 'posts_search.html'
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

class PostAddView(CreateView):
    form_class = PostAddForm
    model = Post
    template_name = "post_add.html"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.post_type = Post.news
        return super().form_valid(f)

class ArticleAddView(CreateView):
    form_class = PostAddForm
    model = Post
    template_name = "post_add.html"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.post_type = Post.article
        return super().form_valid(f)

class PostUpdateView(UpdateView):
    form_class = PostAddForm
    model = Post
    template_name = "post_add.html"

class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('posts_all')
