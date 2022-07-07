from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *
from .services import create_user, shortener


@login_required(login_url='shortener_app:signin')
def index_view(request):
    return HttpResponse('<h1>homepage</h1>')


def signup_view(request):
    """ Регистрация пользователя """
    if request.method != 'POST':
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    else:
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = create_user(user_form=user_form, profile_form=profile_form)
            login(request, user)
            return redirect('shortener_app:index')

    context = {
        'title': 'Регистрация',
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'shortener_app/signup.html', context)


class SignIn(LoginView):
    """ Авторизация пользователя """
    form_class = LoginUserForm
    template_name = 'shortener_app/signin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def get_success_url(self):
        return reverse_lazy('shortener_app:index')


@login_required(login_url='shortener_app:signin')
def logout_view(request):
    """ Выход из аккаунта """
    logout(request)
    return redirect('shortener_app:signin')


@login_required(login_url='shortener_app:signin')
def shortener_view(request):
    """ Сокращатель ссылок """
    if request.method != 'POST':
        form = ShortenerForm(user=request.user)
    else:
        form = ShortenerForm(user=request.user, data=request.POST)
        if form.is_valid():
            short_link = shortener(user=request.user, form=form)
            return render(request, 'shortener_app/link.html', context={'link': short_link})

    context = {
        'title': 'Сокращатель ссылок',
        'form': form,
    }
    return render(request, 'shortener_app/shortener.html', context)


def links_view(request):
    """ Просмотр всех ссылок пользователя """
    user = Profile.objects.get(pk=request.user.profile.pk)
    links = user.shortlink_set.order_by('-date_added')
    context = {
        'title': 'Мои ссылки',
        'links': links
    }
    return render(request, 'shortener_app/my_links.html', context)
