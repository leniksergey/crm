from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from users.mixins import ModelPermissionMixin

from .models import Advertisement

FIELDS = ["name", "product", "channel", "budget"]


class AdListView(ModelPermissionMixin, ListView):
    model = Advertisement
    template_name = "ads/ads-list.html"
    context_object_name = "ads"


class AdDetailView(ModelPermissionMixin, DetailView):
    model = Advertisement
    template_name = "ads/ads-detail.html"


class AdCreateView(ModelPermissionMixin, CreateView):
    model = Advertisement
    fields = FIELDS
    template_name = "ads/ads-create.html"
    success_url = reverse_lazy("ads:list")


class AdUpdateView(ModelPermissionMixin, UpdateView):
    model = Advertisement
    fields = FIELDS
    template_name = "ads/ads-edit.html"

    def get_success_url(self):
        return reverse("ads:detail", kwargs={"pk": self.object.pk})


class AdDeleteView(ModelPermissionMixin, DeleteView):
    model = Advertisement
    template_name = "ads/ads-delete.html"
    success_url = reverse_lazy("ads:list")


class AdStatisticView(LoginRequiredMixin, ListView):
    template_name = "ads/ads-statistic.html"
    context_object_name = "ads"

    def get_queryset(self):
        return Advertisement.objects.annotate(
            leads_count=Count("leads", distinct=True),
            customers_count=Count("leads__customer", distinct=True),
            revenue=Coalesce(
                Sum("leads__customer__contract__cost"),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for ad in context["ads"]:
            if ad.leads_count:
                ad.conversion_rate = (
                    Decimal(ad.customers_count) / Decimal(ad.leads_count) * 100
                ).quantize(Decimal("0.01"))
            else:
                ad.conversion_rate = None
            if ad.budget:
                ad.roas = (ad.revenue / ad.budget).quantize(Decimal("0.01"))
            else:
                ad.roas = None
        return context
