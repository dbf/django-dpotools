from django.conf import settings
from django.shortcuts import render


def alive(response):
    return render(response, "landing/alive.html", {})


def home(response):
    return render(response, "landing/landing.html", {})
