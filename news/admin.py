from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

# напишем функцию добавления рейтинга
def like_three(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    for posts in queryset:
        posts.rating = posts.rating + 3
        posts.save()
like_three.short_description = 'Добавить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект

# создаём новый класс для представления постов в админке
class PostAdmin (admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('heading','data_create','author')
    list_filter = ('data_create','author')# добавляем примитивные фильтры в нашу админку
    search_fields = ('heading',)
    actions = [like_three] #добавляем действия в список

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

# Register your models here.
