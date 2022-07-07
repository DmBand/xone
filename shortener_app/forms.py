from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class ProfileForm(forms.ModelForm):
    """ Форма ввода доменного имени """

    class Meta:
        model = Profile
        fields = ('domain',)

    def clean_domain(self):
        domain = self.cleaned_data.get('domain').strip()
        if Profile.objects.filter(domain__iexact=domain).exists():
            raise ValidationError('Данное доменное имя занято')
        return domain


class LoginUserForm(AuthenticationForm):
    """ Форма авторизации пользователей """
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class ShortenerForm(forms.ModelForm):
    """ Форма создания сокращенной ссылки """

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ShortenerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ShortLink
        fields = ('site_name', 'original_link',)
        widgets = {'original_link': forms.URLInput()}

    def clean_site_name(self):
        site_name = self.cleaned_data.get('site_name')
        profile = Profile.objects.get(pk=self.user.profile.pk)
        if profile.shortlink_set.filter(site_name__iexact=site_name).exists():
            raise ValidationError('У вас уже есть сайт с таким именем')
        return site_name
