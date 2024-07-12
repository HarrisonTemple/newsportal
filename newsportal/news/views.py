import django.contrib.auth.views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from .models import Post
from .filters import PostFilter
from .forms import PostAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect



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

class PostAddView(PermissionRequiredMixin, CreateView):
    form_class = PostAddForm
    model = Post
    template_name = "post_add.html"
    permission_required = 'news.add_post'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.post_type = Post.news
        return super().form_valid(f)

class ArticleAddView(PermissionRequiredMixin, CreateView):
    form_class = PostAddForm
    model = Post
    template_name = "post_add.html"
    permission_required = 'news.add_post'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.post_type = Post.article
        return super().form_valid(f)

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = PostAddForm
    model = Post
    template_name = "post_add.html"
    permission_required = 'news.update_post'

class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('posts_all')
    permission_required = 'news.delete_post'

class UserProfileView(LoginRequiredMixin, TemplateView):
    model = django.contrib.auth.views.UserModel
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')
