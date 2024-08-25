from django.urls import include, path

from .views import IndexView

app_name = "main"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
