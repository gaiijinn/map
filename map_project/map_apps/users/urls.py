from django.urls import path

from .views import users

app_name = "users"


urlpatterns = [
    path("", users, name="users"),
]
