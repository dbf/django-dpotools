from django.urls import path
from . import views

app_name = "landing"

urlpatterns = [
    path("", views.home, name="home"),
    path("alive/", views.alive, name="alive"),
]
