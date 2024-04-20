from django.urls import path

from . import views

# namespace for url in template
app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),

    path("login/", views.login, name="login"),

    path("password-reset/", views.password_reset_email, name="password_reset"),

    path("password-reset/done/", views.password_reset_done, name="password_reset_done"),

    path("reset/done/", views.password_reset_complete, name="password_reset_complete"),

    path("reset/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
]
