from django.urls import path

from .views import users

app_name = 'services'


urlpatterns = [
    path('', users, name='users'),
]
