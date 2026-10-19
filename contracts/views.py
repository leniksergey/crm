from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ContractForm
from .models import Contract
from users.mixins import ModelPermissionMixin


class ContractListView(ModelPermissionMixin, ListView):
    model = Contract
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"


class ContractDetailView(ModelPermissionMixin, DetailView):
    model = Contract
    template_name = "contracts/contracts-detail.html"


class ContractCreateView(ModelPermissionMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    success_url = reverse_lazy("contracts:list")


class ContractUpdateView(ModelPermissionMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-edit.html"

    def get_success_url(self):
        return reverse("contracts:detail", kwargs={"pk": self.object.pk})


class ContractDeleteView(ModelPermissionMixin, DeleteView):
    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:list")