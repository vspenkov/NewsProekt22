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

        # post_author = self.post_set.all()
        # sum_rating_comment_post_author = sum([x['comment_rating'] for x in Comment.objects.filter(post__in=post_author).values()])  - не получается с этим

        self.user_rating = pRat*3+cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'


class Category(models.Model):
    name = models.CharField(max_length=128, unique = True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    CHOISE_CATEGORY = [
        (article, 'Статья' ),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    type_category = models.CharField(max_length=2, choices= CHOISE_CATEGORY, default = news)
    data_create = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through= 'PostCategory')
    heading = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.author}\n {self.type_category}\n {self.data_create}\n {self.post_category}\n {self.heading}\n {self.text}\n {self.rating}'

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


# Create your models here.


