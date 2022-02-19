from celery import shared_task, app
from django.core.mail import send_mail
from celery.schedules import crontab
from .models import User, Post, PostCategory, Category
from datetime import datetime, timedelta


#Таска по отправке дайджеста раз в
@shared_task
def send_week_digest():
    print('Посты за неделю')
    for category in Category.objects.all():
        news_category = []
        week_news = Post.objects.filter(post_category__name=category).filter(
            data_create__range=[datetime.now() - timedelta(days=7), datetime.now()])
        for news in week_news:
            url = f'http://127.0.0.1:8000/news/{news.id} {news.heading} '
            news_category.append(url)


        send_news = '\n'.join(news_category)

        for user in category.subscriber.all():
            sub_send_mail = user.email
            sub_send_name = user.username
            send_mail(
                subject = f'Новости за неделю по категории {sub_send_name}!',
                message = f'Новости за неделю: \n {send_news}',
                from_email = 'vladislav.penkov1993@yandex.ru',
                recipient_list = [sub_send_mail],
            )
