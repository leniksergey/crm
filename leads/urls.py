from django.urls import path, re_path

from . import views

app_name = "leads"

urlpatterns = [
    path("", views.LeadListView.as_view(), name="list"),
    re_path(r"^new/?$", views.LeadCreateView.as_view(), name="create"),
    re_path(r"^(?P<pk>\d+)/?$", views.LeadDetailView.as_view(), name="detail"),
    re_path(r"^(?P<pk>\d+)/edit/?$", views.LeadUpdateView.as_view(), name="edit"),
    re_path(r"^(?P<pk>\d+)/delete/?$", views.LeadDeleteView.as_view(), name="delete"),
]