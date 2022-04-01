from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Author, Category, Post, PostCategory, Comment, User
from datetime import datetime, timedelta
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#для асинхронных задач celery
from .tasks import send_week_digest
from django.utils import timezone
# импортируем наш кэш
from django.core.cache import cache


#Дженерик всех новостей
class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-data_create')
    paginate_by = 10
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):  #забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


#Дженерик подробной новости
class NewsDetail(DetailView):
    model = Post # модель
    template_name = 'news_one.html' # название шаблона
    context_object_name = 'news_one' # название объекта
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.object.pk)
        user = User.objects.get(id=self.request.user.id)
        context['category_all'] = post.post_category.all()
        context['subs_list'] = [i['pk'] for i in user.category_set.all().values('pk')]
        context['subs_list_named'] = [i['name'] for i in user.category_set.all().values('name')]
        return context

    # переопределяем метод получения объекта, как ни странно
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)

        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

#Дженерик добавления поиска
class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'  # название шаблона
    context_object_name = 'search'  # название объекта
    queryset = Post.objects.order_by('-data_create')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

#Дженерик добавления новости
class NewsAdd(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    context_object_name = 'add'
    form_class = PostForm # добавляем форм класс, чтобы получать доступ к форме через метод POST
    permission_required = ('news.add_post',) #Добавляем права

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(authorUser=self.request.user)
        post.save()
        return super().form_valid(form)

    # def send_sub_mail(self, instance):
    #     for category in instance.post_category.all():
    #         subjects = f'Добавлен пост {instance.heading} в {category}'
    #         texts = instance.text[:50]
    #         for user in category.subscriber.all():
    #             sub_mail = user.email
    #             subs_news.delay(subjects, texts, sub_mail)




#Дженерик редактирования новости
class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


#Дженерик удаления
class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',
                           'news.view_post',
                           )

#Дженерик подписки на категорию
class Category_Sub(UpdateView):
    model = Category
    status = None
    fields = []

    def post(self, request, *args, **kwargs):
        status = self.status
        user = self.request.user
        category = Category.objects.get(pk=self.kwargs.get('pk'))
        if status == 'subscribe':
            Category.objects.get(pk = self.kwargs.get('pk')).subscriber.add(user)
            send_mail(
                subject=f'{category.name}',
                message=f'Вы подписались на обновление категории {category.name}',

                from_email='vladislav.penkov1993@yandex.ru',
                recipient_list=[
                    Category.objects.get(pk=self.kwargs.get('pk')).subscriber.get(id=request.user.id).email]
            )
        elif status == 'unsubscribe':
            send_mail(
                subject = f'{category.name}',
                message = f'Вы отписались от обновлений {category.name}',
                from_email= 'vladislav.penkov1993@yandex.ru',
                recipient_list=[
                    Category.objects.get(pk=self.kwargs.get('pk')).subscriber.get(id=request.user.id).email
                ]
            )
            Category.objects.get(pk=self.kwargs.get('pk')).subscriber.remove(user)

        return redirect(request.META.get('HTTP_REFERER'))


def week_digest():
    send_week_digest.delay()
#
#
# week_digest()





# Create your views here.
