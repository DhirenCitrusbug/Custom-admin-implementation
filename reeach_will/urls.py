"""reeach_will URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('admin/',include('admin_user.urls')),
    path('agency/',include('aegency_user.urls')),
    path('',include('client.urls')),
    path('customadmin/',include('customadmin.urls')),

]
handler404 = "reeach_will.views.page_not_found_view"