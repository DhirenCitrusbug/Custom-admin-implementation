from django.urls import path, include
from . import urls_customadmin

urlpatterns = [
    path("", include(urls_customadmin)),
]