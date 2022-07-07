from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class ProfileForm(forms.ModelForm):
    """
    Форма ввода уникального доменного имени
    пользователя при регистрации
    """

    class Meta:
        model = Profile
        fields = ('domain',)

    def clean_domain(self):
        domain = self.cleaned_data['domain'].strip()
        if Profile.objects.filter(domain__iexact=domain).exists():
            raise ValidationError('Данное доменное имя занято')
        return domain


class LoginUserForm(AuthenticationForm):
    """ Форма авторизации пользователей """

    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class ShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = ('site_name', 'original_link',)
        widgets = {'original_link': forms.URLInput()}
