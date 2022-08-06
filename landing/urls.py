from django.urls import path
from . import views

app_name = "landing"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("landing/", views.home, name="landing"),
    path("dpo/", views.home, name="dpo"),
    path("dsb/", views.home, name="dsb"),
]
