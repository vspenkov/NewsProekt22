from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются


@register.filter(name='censor')

def censor(value):
    censor_word = [
        'бля', 'блядь', 'гандон', 'дрочить', 'хуй', 'хуйло', 'шлюха', 'прошмандовка', 'шлюх',
        'пизда', 'еблан', 'манда', 'целка', 'ебать', 'пиздец', 'ебушки-воробушки', 'срать'
    ]
    for i in censor_word:
        value = value.replace(i, 'Цензура')
    return value
