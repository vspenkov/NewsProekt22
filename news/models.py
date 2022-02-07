from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat=0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('comment_rating'))
        cRat=0
        cRat += commentRat.get('commentRating')
        self.user_rating = pRat*3+cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    name = models.CharField(max_length=128, unique = True)
    subscriber = models.ManyToManyField(User, through='CategoryUser')

    def __str__(self):
        return f'{self.name}' #Что мы хотим чтобы выводилось


class CategoryUser(models.Model):
    user_through = models.ForeignKey(User, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    CHOISE_CATEGORY = [
        (article, 'Статья' ),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete = models.CASCADE, verbose_name = "Автор")
    type_category = models.CharField(max_length=2, choices= CHOISE_CATEGORY, default = news, verbose_name = "Категория")
    data_create = models.DateTimeField(auto_now_add=True, verbose_name = "Дата создания")
    post_category = models.ManyToManyField(Category, through= 'PostCategory')
    heading = models.CharField(max_length = 128, verbose_name = "Заголовок")
    text = models.TextField(verbose_name = "Содержание")
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.author}\n {self.type_category}\n {self.data_create}\n {self.post_category.all()}\n {self.heading}\n {self.text}\n {self.rating}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + "..."


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete = models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete = models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 1000)
    comment_create = models.DateTimeField(auto_now_add = True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating +=1
        self.save()

    def dislike(self):
        self.comment_rating -=1
        self.save()


