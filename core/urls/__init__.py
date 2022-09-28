from django.urls import path, include
from . import urls_core,  urls_auth

urlpatterns = [
    path("", include(urls_core)),
    path("", include(urls_auth)),
]