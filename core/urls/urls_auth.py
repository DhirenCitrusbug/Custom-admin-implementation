from django.contrib.auth import views as auth_views
from django.urls import path, re_path

app_name = 'auth'
urlpatterns = [

    # Login / Logout
    path("login/", auth_views.LoginView.as_view(template_name='core/ebr/registration/login.html'), name="auth_login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        {'next_page': 'auth:auth_login'},  # redirect user
        name="auth_logout",
    ),
    # Password Change
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(),
        name="auth_password_change",
    ),
    path(
        "password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Password reset
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(),
        name="auth_password_reset",
    ),
    re_path(
        r"^auth_password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        auth_views.PasswordResetConfirmView.as_view(),
        name="auth_password_reset_confirm",
    ),
    path(
        "auth_password/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "auth_password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
]