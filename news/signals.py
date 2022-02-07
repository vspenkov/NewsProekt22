from django.db.models.signals import m2m_changed #связь так-как две модели импортируем. Одна для поста, вторая для списка контактов
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post

@receiver(m2m_changed, sender = Post.post_category.through)
def subs_news(sender, instance, **kwargs):
    for category in instance.post_category.all():
        subjects = f'Добавлен пост {instance.heading} в {category}'
        texts = instance.text[:50]
        for user in category.subscriber.all():
            send_mail(
                subject=subjects,
                message=texts,
                from_email='vladislav.penkov1993@yandex.ru',
                recipient_list=[user.email]
            )

