"""dpotools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

if "shibboleth" in settings.INSTALLED_APPS:
    from shibboleth.views import ShibbolethLoginView, ShibbolethLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("contact/", include("contact.urls")),
    path("rpa/", include("rpa.urls")),
    path("breach/", include("breach.urls")),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

if "shibboleth" in settings.INSTALLED_APPS:
    urlpatterns += [
        path("login", ShibbolethLoginView.as_view(), name="login"),
        path("logout", ShibbolethLogoutView.as_view(), name="logout"),
        re_path(r"^shib/", include("shibboleth.urls", namespace="shibboleth")),
    ]
else:
    urlpatterns += [
        path("login", auth_views.LoginView.as_view(), name="login"),
        path("logout", auth_views.LogoutView.as_view(), name="logout"),
    ]

urlpatterns += [
    path("", include("landing.urls")),
]
