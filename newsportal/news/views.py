import django.contrib.auth.views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category, CategorySubscribers, Author
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

    def post(self, request, *args, **kwargs):
        cat = request.POST['category']
        if request.user is not None:
            if not Category.objects.filter(cat_name=cat).filter(subscribers=request.user).exists():
                sub = CategorySubscribers(
                    subscribers=request.user,
                    category=Category.objects.get(cat_name=cat)
                )
                sub.save()
        return redirect(request.get_full_path())

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
        f.post_type = Post.news
        f.author = Author.objects.get(user_ref=self.request.user)
        f.save()
        form.save_m2m()

        site = self.request.build_absolute_uri(f.get_absolute_url())
        meta = {'link': site}
        html = render_to_string('mailing/new post.html', {'post': f, 'meta': meta})

        recipients = [x['subscribers__email'] for x in CategorySubscribers.objects.filter(category__in=f.category.all()).exclude(subscribers__email__isnull=True).exclude(subscribers__email__exact='').values('subscribers__email')]
        cats = ", ".join([x['cat_name'] for x in f.category.all().values('cat_name')])

        message = EmailMultiAlternatives(
            subject=f'New article in {cats} categories!',
            body=f.content[:150] + '...',
            from_email='daniilka1995@ya.ru',
            to=recipients
        )
        message.attach_alternative(html, 'text/html')
        message.send()
        return super().form_valid(form)

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
        context['categories'] = Category.objects.filter(subscribers=self.request.user)
        return context


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')

    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)

    if Author.objects.filter(user_ref=user).first() is None:
        author = Author(user_ref=user)
        author.save()

    return redirect('/')
