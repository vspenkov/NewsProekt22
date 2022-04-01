from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsAdd, NewsUpdate, NewsDelete,Category_Sub
from django.views.decorators.cache import cache_page


urlpatterns = [
# path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('',cache_page(60)(NewsList.as_view())), # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>',NewsDetail.as_view()), # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search/', NewsSearch.as_view(), name='search'),
    path('add/', NewsAdd.as_view(), name='add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='delete'),
    path('category/<int:pk>/add/', Category_Sub.as_view(status='subscribe'), name='subscribe'),
    path('category/<int:pk>/remove/', Category_Sub.as_view(status='unsubscribe'), name='unsubscribe')
]