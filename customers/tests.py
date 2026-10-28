from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from ads.models import Advertisement
from contracts.models import Contract
from leads.models import Lead
from products.models import Product

from .forms import CustomerForm
from .models import Customer


class CustomerFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = Product.objects.create(
            name="Услуга",
            cost=Decimal("1000.00"),
        )
        advertisement = Advertisement.objects.create(
            name="Кампания",
            product=product,
            channel="VK",
            budget=Decimal("5000.00"),
        )
        cls.new_lead = Lead.objects.create(
            last_name="Иванов",
            first_name="Иван",
            phone="+79000000001",
            email="new@example.com",
            ad=advertisement,
            status=Lead.Status.NEW,
        )
        cls.won_lead = Lead.objects.create(
            last_name="Петров",
            first_name="Пётр",
            phone="+79000000002",
            email="won@example.com",
            ad=advertisement,
            status=Lead.Status.WON,
        )
        converted_lead = Lead.objects.create(
            last_name="Сидоров",
            first_name="Сидор",
            phone="+79000000003",
            email="converted@example.com",
            ad=advertisement,
            status=Lead.Status.WON,
        )
        contract = Contract.objects.create(
            name="Договор",
            product=product,
            file="contracts/contract.txt",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            cost=Decimal("1000.00"),
        )
        Customer.objects.create(lead=converted_lead, contract=contract)

    def test_only_successful_unconverted_leads_are_available(self):
        available_leads = list(CustomerForm().fields["lead"].queryset)

        self.assertEqual(available_leads, [self.won_lead])

    def test_customer_cannot_be_created_from_unsuccessful_lead(self):
        contract = Contract.objects.first()
        customer = Customer(lead=self.new_lead, contract=contract)

        with self.assertRaises(ValidationError):
            customer.full_clean()
