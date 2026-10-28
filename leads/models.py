from django.db import models

from ads.models import Advertisement


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        CONTACTED = "contacted", "Связались"
        NEGOTIATION = "negotiation", "Переговоры"
        WON = "won", "Успешно"
        LOST = "lost", "Отказ"

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
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def can_convert_to_customer(self):
        return self.status == self.Status.WON and not hasattr(self, "customer")
