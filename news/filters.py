from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Author, Category, Post, PostCategory, Comment
from django.forms import DateInput

# создаём фильтр
# Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах

class PostFilter(FilterSet):
    author = ModelMultipleChoiceFilter('author',
        lookup_expr='exact',
        label='Автор',
        queryset= Author.objects.all()
    )

    title = CharFilter(
        field_name='heading',
        lookup_expr='icontains',
        label='Заголовок'
    )
    datetime = DateFilter(
        field_name='data_create',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Позже даты'
    )

    class Meta:
        model = Post
        fields = []
  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)