from django.urls import path
from .views import login, login_redirect, logout, logout_redirect

urlpatterns = [
    path("login", login),
    path("login_redirect", login_redirect),
    path("logout", logout),
    path("logout_redirect", logout_redirect),
]
