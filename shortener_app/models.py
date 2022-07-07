from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """ Модель профиля пользователя """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domain = models.CharField(verbose_name='доменное имя', max_length=30)

    def __str__(self):
        return self.domain


class ShortLink(models.Model):
    """ Модель сокращенной ссылки """
    site_name = models.CharField(verbose_name='название сайта', max_length=50)
    original_link = models.URLField(verbose_name='оригинальная ссылка', max_length=1000)
    short_link = models.CharField(verbose_name='сокращенная ссылка', max_length=50)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.site_name
