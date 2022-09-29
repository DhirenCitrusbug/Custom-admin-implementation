from sunau import Au_read
from django.urls import path

from .views import IndexView,AgencyListView,ClientListView,AgencyUpdateView,ClientUpdateView,AgencyDeleteView,ClientDeleteView
from django.contrib.auth import views as auth_views
app_name='core'
urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path("login/", auth_views.LoginView.as_view(template_name='core/ebr/registration/login.html'), name="auth_login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='core/ebr/registration/logout.html'), name="auth_logout"),
    path('agency-list/',AgencyListView.as_view(),name='agency-list'),
    path('client-list/',ClientListView.as_view(),name='client-list'),
    path('agency-change/<int:pk>',AgencyUpdateView.as_view(),name='agency-update'),
    path('client-change/<int:pk>',ClientUpdateView.as_view(),name='client-update'),
    path('agency-delete/<int:pk>',AgencyDeleteView.as_view(),name='agency-delete'),
    path('client-delete/<int:pk>',ClientDeleteView.as_view(),name='client-delete'),

]


