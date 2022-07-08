from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import ShortLink


class UserForm(UserCreationForm):
    class Meta: 
        model = User
        fields = {
            'username', 'password1', 'password2'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input'})


class LoginUserForm(AuthenticationForm):
    """ Форма авторизации пользователей """
    username = forms.CharField(
        label='Логин', 
        widget=forms.TextInput(
            attrs={'class': 'input'}
        )
    )
    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(
            attrs={'class': 'input'}
        )
    )


class ShortenerForm(forms.ModelForm):
    """ Форма создания сокращенной ссылки """

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ShortenerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ShortLink
        fields = ('site_name', 'original_link',)
        widgets = {
            'site_name': forms.TextInput(
                attrs={'class': 'input'}
            ),
            'original_link': forms.URLInput(
                attrs={'class': 'input'}
            )
        }

    def clean_site_name(self):
        site_name = self.cleaned_data.get('site_name')
        profile = User.objects.get(pk=self.user.pk)
        if profile.shortlink_set.filter(site_name__iexact=site_name).exists():
            raise ValidationError('У вас уже есть сайт с таким названием')
        return site_name
