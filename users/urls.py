from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
]