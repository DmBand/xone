import string
import random

from .models import *


def create_user(user_form, profile_form):
    """ Создание нового пользователя """
    user = user_form.save()
    profile = profile_form.save(commit=False)
    profile.slug = user.username
    profile.user = user
    profile.save()
    return user


def create_shortlink(form, short_link, user):
    """ Создает в БД новую сокращенную ссылку """
    new_short_link = ShortLink.objects.create(
        site_name=form.cleaned_data.get('site_name'),
        original_link=form.cleaned_data.get('original_link'),
        short_link=short_link,
        owner=user.profile
    )
    return new_short_link


def url_generator(user, form):
    """ Генерирует сокращенную ссылку и возвращает её"""
    symbols = list(string.ascii_letters) + [str(i) for i in range(1, 10)]
    url = ''.join([random.choice(symbols) for _ in range(5)])
    protocol = 'http://' if 'http:' in form.cleaned_data.get('original_link')[:6] else 'https://'
    short_link = f'{protocol}{user.profile.domain}/{url}'
    return short_link


def unique_url(user, form):
    """ Возвращает уникальную сокращенную ссылку """
    profile = Profile.objects.get(pk=user.profile.pk)
    new_link = url_generator(user=user, form=form)
    while True:
        if profile.shortlink_set.filter(short_link__iexact=new_link).exists():
            new_link = url_generator(user=user, form=form)
        else:
            return new_link


def shortener(user, form):
    """ СОздает уникальную сокращенную ссылку и сохраняет её в БД """
    url = unique_url(user=user, form=form)
    create_shortlink(form=form, short_link=url, user=user)
    return url
