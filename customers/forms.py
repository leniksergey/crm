from django import forms
from django.db.models import Q

from leads.models import Lead

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["lead", "contract"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available = Q(customer__isnull=True)
        if self.instance.pk:
            available |= Q(pk=self.instance.lead_id)
        self.fields["lead"].queryset = Lead.objects.filter(available)