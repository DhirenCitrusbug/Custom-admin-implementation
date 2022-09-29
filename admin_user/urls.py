from django.contrib import admin
from django.urls import path, include
from .views import (AdminUserLoginView,IndexView,AdminUserLogoutView,AdminEditView,
                    AdminUserListView,AgencyActiveUser,AgencyEditView,AgencyDeleteView,StatusWiseFilter,AdminDashboardFilterView)
urlpatterns = [
   path('',AdminUserLoginView.as_view(),name="admin-login"),
   path('admin-logout/',AdminUserLogoutView.as_view(),name="admin-logout"),
   path('admin-setting/',AdminEditView.as_view(),name="admin-setting"),
   path('agency-list/',AdminUserListView.as_view(),name="admin-user"),
   path('agency-active/',AgencyActiveUser,name="agency-active"),
   path('agency-edit/',AgencyEditView.as_view(),name="agency-edit"),
   path('agency-delete/<str:id>',AgencyDeleteView.as_view(),name="agency-delete"),
   path('status-agency/',StatusWiseFilter.as_view(),name="status-agency"),
   path('admin-dashboard-filter/',AdminDashboardFilterView.as_view(),name="admin-dashboard-filter"),
   path('admin-dashboard/',IndexView.as_view(),name="index"),
]
