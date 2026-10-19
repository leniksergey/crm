from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CustomerForm
from .models import Customer
from users.mixins import ModelPermissionMixin



class CustomerListView(ModelPermissionMixin, ListView):
    model = Customer
    template_name = "customers/customers-list.html"
    context_object_name = "customers"


class CustomerDetailView(ModelPermissionMixin, DetailView):
    model = Customer
    template_name = "customers/customers-detail.html"


class CustomerCreateView(ModelPermissionMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customers-create.html"
    success_url = reverse_lazy("customers:list")

    def get_initial(self):
        initial = super().get_initial()
        lead_id = self.request.GET.get("lead")
        if lead_id:
            initial["lead"] = lead_id
        return initial


class CustomerUpdateView(ModelPermissionMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customers-edit.html"

    def get_success_url(self):
        return reverse("customers:detail", kwargs={"pk": self.object.pk})


class CustomerDeleteView(ModelPermissionMixin, DeleteView):
    model = Customer
    template_name = "customers/customers-delete.html"
    success_url = reverse_lazy("customers:list")