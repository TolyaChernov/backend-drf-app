from django.urls import path

from .views import (ChangePasswordView, UserLoginView, UserLogoutView,
                    UserRegisterView)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change_password"),
]
