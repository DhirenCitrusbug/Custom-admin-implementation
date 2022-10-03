from django.urls import path, include
from . import urls_customadmin,urls_auth

urlpatterns = [
    path("", include(urls_auth)),
    path("", include(urls_customadmin)),
]