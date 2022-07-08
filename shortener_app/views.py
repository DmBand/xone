from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *
from .services import shortener


@login_required(login_url='shortener_app:signin')
def shortener_view(request):
    """ Сокращатель ссылок """
    if request.method != 'POST':
        form = ShortenerForm(user=request.user)
    else:
        form = ShortenerForm(user=request.user, data=request.POST)
        if form.is_valid():
            protocol = 'https://' if request.is_secure() else 'http://'
            prefix = f'{protocol}{request.META["HTTP_HOST"]}/'
            short_link = shortener(user=request.user, form=form)
            context = {
                'title': 'Готовая ссылка',
                'link': f'{prefix}{short_link}'
            }
            return render(request, 'shortener_app/link.html', context)

    context = {
        'title': 'Сокращатель ссылок',
        'form': form,
    }
    return render(request, 'shortener_app/shortener.html', context)


def signup_view(request):
    """ Регистрация пользователя """
    if request.method != 'POST':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shortener_app:shortener')

    context = {
        'title': 'Регистрация',
        'form': form,
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
        return reverse_lazy('shortener_app:shortener')


@login_required(login_url='shortener_app:signin')
def logout_view(request):
    """ Выход из аккаунта """
    logout(request)
    return redirect('shortener_app:signin')


@login_required(login_url='shortener_app:signin')
def links_view(request):
    """ Просмотр всех ссылок пользователя """
    user = User.objects.get(pk=request.user.pk)
    links = user.shortlink_set.order_by('-date_added')
    context = {
        'title': 'Мои ссылки',
        'links': links
    }
    return render(request, 'shortener_app/my_links.html', context)


def redirect_view(request, link):
    """ Редирект на оригинальную страницу """
    link_ = ShortLink.objects.filter(owner=request.user.pk, short_link=link)
    if link_:
        url = link_.values()[0].get('original_link')
        return redirect(url)
    raise Http404('Нет такой ссылки')
