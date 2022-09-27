from django.contrib import admin
from django.urls import path, include
from .viewss import AgencyDashboardView,AgencyUserLogoutView,\
AgencyTwillioView,ClientActiveUser,ClientDeleteView,AgencyChangePasswordView,AgencyWhitelabelSettingView,AgencyWhitelabeldomianCheckView
from .views.agency_login import AgencyUserLoginView
from .views.agency_logout import AgencyUserLogoutView
from .views.agency_setting import AgencySettingView
from .views.agency_forgot_password import AgencyForgetPasswordView
from .views.agency_set_password import AgencySetPasswordView
from .views.add_client import AddClientView
from .views.country_wise_state import CountryWiseState
from .views.client_search import ClientSearch
from .views.country import CountryView
urlpatterns = [
   path('agency-login/',AgencyUserLoginView.as_view(),name="agency-login"),
   path('agency-dashboard/',AgencyDashboardView.as_view(),name="agency-dashboard"),
   path('agency-logout/',AgencyUserLogoutView.as_view(),name="agency-logout"),
   path('agency-settings/',AgencySettingView.as_view(),name='agency-setting'),
   path('agency-forget-password/',AgencyForgetPasswordView.as_view(),name="agency-forget-password"),
   path('reset-password/<str:uuid>/',AgencySetPasswordView.as_view(),name="reset_password"),
   path('addclient/',AddClientView.as_view(),name="add_client"),
   path('country-state/',CountryWiseState.as_view(),name="country-state"),
   path('client-search/',ClientSearch.as_view(),name="client-search"),
   path('country/',CountryView.as_view(),name="country"),
   path('agency-twillio/',AgencyTwillioView.as_view(),name="agency-twillio"),
   path('client-active/',ClientActiveUser,name="client-active"),
   path('client-delete/<str:id>/',ClientDeleteView.as_view(),name="client-delete"),
   path('agency-change-password/',AgencyChangePasswordView.as_view(),name="agency-change-password"),
   path('agency-whitelabel-setting/',AgencyWhitelabelSettingView.as_view(),name="agency-whitelabel-setting"),
   path('agency-whitelabel-detail/',AgencyWhitelabeldomianCheckView.as_view(),name="agency_whitelabel_detail"),

]
