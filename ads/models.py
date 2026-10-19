from django.db import models

from products.models import Product


class Advertisement(models.Model):
    name = models.CharField("Название", max_length=200)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="ads", verbose_name="Услуга"
    )
    channel = models.CharField("Канал продвижения", max_length=200)
    budget = models.DecimalField("Бюджет", max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.name)