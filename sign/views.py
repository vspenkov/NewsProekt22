from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from news.models import Author
from django.contrib.auth.decorators import login_required




from django.contrib.auth.decorators import login_required #проверка аутинфикации


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required #функция-представления
def upgrade_me(request='user'):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)

    if not Author.objects.filter(authorUser=request.user).exists():
        Author.objects.create(authorUser=request.user)
    return redirect('/member/')

# Create your views here.
