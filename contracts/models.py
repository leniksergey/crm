from django.db import models

from products.models import Product


class Contract(models.Model):
    name = models.CharField("Название", max_length=200)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="contracts",
        verbose_name="Услуга",
    )
    file = models.FileField("Файл договора", upload_to="contracts/")
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    cost = models.DecimalField("Сумма", max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.name)