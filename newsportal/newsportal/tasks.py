from celery import shared_task
import datetime
from django.contrib.sites.models import Site
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, CategorySubscribers

@shared_task
def new_post_notification(content_delegate):
    content_delegate()

@shared_task
def weekly_messaging():
    for user in User.objects.all():
        if user.email != "":
            cats = CategorySubscribers.objects.filter(subscribers=user).values('category')
            posts = Post.objects.filter(category__in=cats,
                                        publish_date__gt=datetime.datetime.now() - datetime.timedelta(days=7))
            posts_w_links = [(post, Site.objects.get_current().domain + reverse('post_detail', args=[str(post.id)])) for
                             post in posts]
            cont = {'posts': posts_w_links}
            html = render_to_string('mailing/weekly.html', context=cont)
            message = EmailMultiAlternatives(
                subject=f'There is {len(posts)} new posts in categories you follow! ',
                from_email='daniilka1995@ya.ru',
                to=[user.email],
            )
            message.attach_alternative(html, "text/html")
            message.send()
