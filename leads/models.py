from django.db import models

from ads.models import Advertisement


class Lead(models.Model):
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email")
    ad = models.ForeignKey(
        Advertisement,
        on_delete=models.PROTECT,
        related_name="leads",
        verbose_name="Рекламная кампания",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"