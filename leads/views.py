from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Lead
from users.mixins import ModelPermissionMixin


FIELDS = ["last_name", "first_name", "phone", "email", "ad"]


class LeadListView(ModelPermissionMixin, ListView):
    model = Lead
    template_name = "leads/leads-list.html"
    context_object_name = "leads"


class LeadDetailView(ModelPermissionMixin, DetailView):
    model = Lead
    template_name = "leads/leads-detail.html"


class LeadCreateView(ModelPermissionMixin, CreateView):
    model = Lead
    fields = FIELDS
    template_name = "leads/leads-create.html"
    success_url = reverse_lazy("leads:list")


class LeadUpdateView(ModelPermissionMixin, UpdateView):
    model = Lead
    fields = FIELDS
    template_name = "leads/leads-edit.html"

    def get_success_url(self):
        return reverse("leads:detail", kwargs={"pk": self.object.pk})


class LeadDeleteView(ModelPermissionMixin, DeleteView):
    model = Lead
    template_name = "leads/leads-delete.html"
    success_url = reverse_lazy("leads:list")