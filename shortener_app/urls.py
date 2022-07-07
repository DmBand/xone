from django.urls import path
from .views import *


app_name = 'shortener_app'
urlpatterns = [
    path('', index_view, name='index'),
    path('signup/', signup_view, name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('logout/', logout_view, name='logout'),
    path('shortener/', shortener_view, name='shortener'),
    path('my_links/', links_view, name='links'),
]
