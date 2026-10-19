from django.urls import path, re_path

from . import views

app_name = "ads"

urlpatterns = [
    path("", views.AdListView.as_view(), name="list"),
    re_path(r"^new/?$", views.AdCreateView.as_view(), name="create"),
    re_path(r"^statistic/?$", views.AdStatisticView.as_view(), name="statistic"),
    re_path(r"^(?P<pk>\d+)/?$", views.AdDetailView.as_view(), name="detail"),
    re_path(r"^(?P<pk>\d+)/edit/?$", views.AdUpdateView.as_view(), name="edit"),
    re_path(r"^(?P<pk>\d+)/delete/?$", views.AdDeleteView.as_view(), name="delete"),
]