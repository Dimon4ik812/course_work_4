from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    BlockUserView,
    ChangePasswordView,
    PasswordResetView,
    RegisterView,
    UserDetailView,
    UserListView,
    email_verification,
)

app_name = "users"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="newapp:home"), name="logout"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_block/<int:user_id>", BlockUserView.as_view(), name="user_block"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("profile/<int:pk>", UserDetailView.as_view(), name="user_profile"),
]
