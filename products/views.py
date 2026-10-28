from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Product
from users.mixins import ModelPermissionMixin

FIELDS = ["name", "description", "cost"]


class ProductListView(ModelPermissionMixin, ListView):
    model = Product
    template_name = "products/products-list.html"
    context_object_name = "products"


class ProductDetailView(ModelPermissionMixin, DetailView):
    model = Product
    template_name = "products/products-detail.html"


class ProductCreateView(ModelPermissionMixin, CreateView):
    model = Product
    fields = FIELDS
    template_name = "products/products-create.html"
    success_url = reverse_lazy("products:list")


class ProductUpdateView(ModelPermissionMixin, UpdateView):
    model = Product
    fields = FIELDS
    template_name = "products/products-edit.html"

    def get_success_url(self):
        return reverse("products:detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(ModelPermissionMixin, DeleteView):
    model = Product
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:list")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Нельзя удалить услугу, на которую ссылаются рекламные кампании или контракты. "
                "Сначала удалите или отвяжите зависимые объекты.",
            )
            return self.render_to_response(self.get_context_data(object=self.object))
