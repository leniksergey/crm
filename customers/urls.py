from django.urls import path, re_path

from . import views

app_name = "customers"

urlpatterns = [
    path("", views.CustomerListView.as_view(), name="list"),
    re_path(r"^new/?$", views.CustomerCreateView.as_view(), name="create"),
    re_path(r"^(?P<pk>\d+)/?$", views.CustomerDetailView.as_view(), name="detail"),
    re_path(r"^(?P<pk>\d+)/edit/?$", views.CustomerUpdateView.as_view(), name="edit"),
    re_path(r"^(?P<pk>\d+)/delete/?$", views.CustomerDeleteView.as_view(), name="delete"),
]