from django.db import models


class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.name)