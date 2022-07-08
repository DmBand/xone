from django.urls import path
from .views import shortener_view, \
    signup_view, \
    SignIn, \
    logout_view, \
    links_view, \
    redirect_view

app_name = 'shortener_app'
urlpatterns = [
    path('', shortener_view, name='shortener'),
    path('signup/', signup_view, name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('logout/', logout_view, name='logout'),
    path('my_links/', links_view, name='links'),
    path('<slug:link>/', redirect_view, name='redirect'),
]
