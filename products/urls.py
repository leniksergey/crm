from django.urls import path, re_path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    re_path(r"^new/?$", views.ProductCreateView.as_view(), name="create"),
    re_path(r"^(?P<pk>\d+)/?$", views.ProductDetailView.as_view(), name="detail"),
    re_path(r"^(?P<pk>\d+)/edit/?$", views.ProductUpdateView.as_view(), name="edit"),
    re_path(r"^(?P<pk>\d+)/delete/?$", views.ProductDeleteView.as_view(), name="delete"),
]