import string
import random

from .models import *


def create_shortlink(form, short_link, user):
    """ Создает в БД новую сокращенную ссылку """
    new_short_link = ShortLink.objects.create(
        site_name=form.cleaned_data.get('site_name'),
        original_link=form.cleaned_data.get('original_link'),
        short_link=short_link,
        owner=user
    )
    return new_short_link


def url_generator():
    """ Генерирует сокращенную ссылку и возвращает её"""
    symbols = list(string.ascii_letters) + [str(i) for i in range(1, 10)]
    url = ''.join([random.choice(symbols) for _ in range(5)])
    return url


def unique_url(user):
    """ Возвращает уникальную сокращенную ссылку """
    profile = User.objects.get(pk=user.pk)
    new_link = url_generator()
    while True:
        if profile.shortlink_set.filter(short_link__iexact=new_link).exists():
            new_link = url_generator()
        else:
            return new_link


def shortener(user, form):
    """ СОздает уникальную сокращенную ссылку и сохраняет её в БД """
    url = unique_url(user=user)
    create_shortlink(form=form, short_link=url, user=user)
    return url
