import datetime
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, CategorySubscribers

logger = logging.getLogger(__name__)

def my_job():

    for user in User.objects.all():
        if user.email != "":
            cats = CategorySubscribers.objects.filter(subscribers=user).values('category')
            posts = Post.objects.filter(category__in=cats, publish_date__gt=datetime.datetime.now() - datetime.timedelta(days=7))
            posts_w_links = [(post, Site.objects.get_current().domain + reverse('post_detail', args=[str(post.id)])) for post in posts]
            cont = {'posts': posts_w_links}
            html = render_to_string('mailing/weekly.html', context=cont)
            message = EmailMultiAlternatives(
                subject=f'There is {len(posts)} new posts in categories you follow! ',
                from_email='daniilka1995@ya.ru',
                to=[user.email],
            )
            message.attach_alternative(html, "text/html")
            message.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="06", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")