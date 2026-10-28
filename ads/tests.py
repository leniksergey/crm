from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from products.models import Product

from .models import Advertisement


class AdvertisementStatisticTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="statistic-user", password="password123"
        )
        product = Product.objects.create(name="Услуга", cost=Decimal("1000.00"))
        cls.advertisement = Advertisement.objects.create(
            name="Кампания",
            product=product,
            channel="VK",
            budget=Decimal("100.00"),
        )
        won_lead = Lead.objects.create(
            last_name="Иванов",
            first_name="Иван",
            phone="+79000000001",
            email="won@example.com",
            ad=cls.advertisement,
            status=Lead.Status.WON,
        )
        Lead.objects.create(
            last_name="Петров",
            first_name="Пётр",
            phone="+79000000002",
            email="new@example.com",
            ad=cls.advertisement,
            status=Lead.Status.NEW,
        )
        contract = Contract.objects.create(
            name="Договор",
            product=product,
            file="contracts/contract.txt",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            cost=Decimal("150.00"),
        )
        Customer.objects.create(lead=won_lead, contract=contract)

    def test_statistic_contains_conversion_revenue_and_roas(self):
        self.client.force_login(self.user)

        response = self.client.get("/ads/statistic")
        advertisement = response.context["ads"].get(pk=self.advertisement.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(advertisement.leads_count, 2)
        self.assertEqual(advertisement.customers_count, 1)
        self.assertEqual(advertisement.revenue, Decimal("150.00"))
        self.assertEqual(advertisement.conversion_rate, Decimal("50.00"))
        self.assertEqual(advertisement.roas, Decimal("1.50"))
