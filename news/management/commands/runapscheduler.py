import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category, CategoryUser, PostCategory
from django.utils import timezone
from datetime import datetime, timedelta


from django.core.mail import EmailMultiAlternatives, send_mail


logger = logging.getLogger(__name__)


def my_job():

    for category in Category.objects.all():
        news_category = []
        week_news = Post.objects.filter(post_category__name = category).filter(data_create__range=[datetime.now() - timedelta(days=7), datetime.now()])
        for news in week_news:
            url = f'http://127.0.0.1:8000/news/{news.id} {news.heading} '
            news_category.append(url)
        send_news = '\n'.join(news_category)


        for user in category.subscriber.all():
            send_mail(
                        f'Новости за неделю по категории {category}!',
                        f'Новости за неделю: \n {send_news}',
                        from_email='vladislav.penkov1993@yandex.ru',
                        recipient_list=[user.email],
                    )


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="10", minute="00"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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