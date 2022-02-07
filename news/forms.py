from django.forms import ModelForm, BooleanField
from .models import Post

# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Вы не робот')
# в класс мета, как обычно, надо написать модель,
# по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Post
        fields = ['heading',
                  'type_category',
                  'post_category',
                  'text',
                  'check_box'
                  ]
        labels = {
            'heading' : 'Заголовок',
            'type_category' : 'Тип',
            'post_category' : 'Категория',
            'text' : 'Текст'
        }