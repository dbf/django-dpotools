from django.conf import settings
from django.shortcuts import render


def home(response):
    return render(response, "landing/landing.html", {})


def landing(response):
    return render(response, "landing/landing.html", {})


def dpo(response):
    return render(response, "landing/landing.html", {})


def dsb(response):
    return render(response, "landing/landing.html", {})
