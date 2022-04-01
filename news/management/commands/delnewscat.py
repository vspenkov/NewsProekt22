from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category, CategoryUser, PostCategory


class Command(BaseCommand):
    help = 'Удаление новостей в категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    # requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options): # здесь можете писать любой код, который выполнется при вызове вашей команды
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(post_category = category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR('Could not find category'))