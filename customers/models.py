from django.db import models
from django.core.exceptions import ValidationError

from contracts.models import Contract
from leads.models import Lead


class Customer(models.Model):
    lead = models.OneToOneField(
        Lead, on_delete=models.PROTECT, verbose_name="Потенциальный клиент"
    )
    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        related_name="customers",
        verbose_name="Контракт",
    )

    def __str__(self):
        return str(self.lead)

    def clean(self):
        super().clean()
        if self.lead_id and self.lead.status != Lead.Status.WON:
            raise ValidationError(
                {"lead": "В активного клиента можно перевести только успешный лид."}
            )
