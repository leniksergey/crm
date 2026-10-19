from django.urls import path, re_path

from . import views

app_name = "contracts"

urlpatterns = [
    path("", views.ContractListView.as_view(), name="list"),
    re_path(r"^new/?$", views.ContractCreateView.as_view(), name="create"),
    re_path(r"^(?P<pk>\d+)/?$", views.ContractDetailView.as_view(), name="detail"),
    re_path(r"^(?P<pk>\d+)/edit/?$", views.ContractUpdateView.as_view(), name="edit"),
    re_path(r"^(?P<pk>\d+)/delete/?$", views.ContractDeleteView.as_view(), name="delete"),
]