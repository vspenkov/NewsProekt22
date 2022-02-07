from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm #импортировали класс формы, который предоставляет allauth
from django.contrib.auth.models import Group #добавили модуль групп


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request) #вызываем этот же метод класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены
        common_group = Group.objects.get(name = 'common') #Далее мы получаем объект модели группы common
        common_group.user_set.add(user) #4ерез атрибут user_set, возвращающий список всех пользователей этой группы
        return user

# Create your models here.
