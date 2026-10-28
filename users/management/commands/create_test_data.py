import os
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal

from products.models import Product
from ads.models import Advertisement
from leads.models import Lead
from contracts.models import Contract
from customers.models import Customer


class Command(BaseCommand):
    help = "Создаёт тестовые данные для CRM (услуги, кампании, лиды, контракты, клиенты)"

    def handle(self, *args, **options):
        # 1. Услуги (3 шт.)
        products_data = [
            {
                "name": "Контекстная реклама",
                "description": "Настройка и ведение рекламы в поисковых системах",
                "cost": Decimal("15000.00"),
            },
            {
                "name": "SMM-продвижение",
                "description": "Ведение социальных сетей и таргетированная реклама",
                "cost": Decimal("25000.00"),
            },
            {
                "name": "SEO оптимизация",
                "description": "Техническая и контентная оптимизация сайта",
                "cost": Decimal("35000.00"),
            },
        ]
        products = []
        for p in products_data:
            product, created = Product.objects.get_or_create(
                name=p["name"],
                defaults={"description": p["description"], "cost": p["cost"]},
            )
            products.append(product)
            self.stdout.write(
                f"Продукт '{product.name}': {'создан' if created else 'уже существует'}"
            )

        # 2. Рекламные кампании (2 шт.)
        ads_data = [
            {
                "name": "Весенняя акция 2026",
                "product": products[0],
                "channel": "VK",
                "budget": Decimal("50000.00"),
            },
            {
                "name": "Ногодняя распродажа",
                "product": products[1],
                "channel": "Telegram",
                "budget": Decimal("75000.00"),
            },
        ]
        ads = []
        for a in ads_data:
            advertisement, created = Advertisement.objects.get_or_create(
                name=a["name"],
                defaults={
                    "product": a["product"],
                    "channel": a["channel"],
                    "budget": a["budget"],
                },
            )
            ads.append(advertisement)
            self.stdout.write(
                f"Кампания '{advertisement.name}': {'создана' if created else 'уже существует'}"
            )

        # 3. Лиды (5 шт.)
        leads_data = [
            {
                "last_name": "Иванов",
                "first_name": "Иван",
                "phone": "+79001112233",
                "email": "ivanov@example.com",
                "ad": ads[0],
                "status": Lead.Status.WON,
            },
            {
                "last_name": "Петров",
                "first_name": "Петр",
                "phone": "+79001112244",
                "email": "petrov@example.com",
                "ad": ads[0],
                "status": Lead.Status.NEGOTIATION,
            },
            {
                "last_name": "Сидорова",
                "first_name": "Анна",
                "phone": "+79001112255",
                "email": "sidorova@example.com",
                "ad": ads[1],
                "status": Lead.Status.WON,
            },
            {
                "last_name": "Козлов",
                "first_name": "Дмитрий",
                "phone": "+79001112266",
                "email": "kozlov@example.com",
                "ad": ads[1],
                "status": Lead.Status.CONTACTED,
            },
            {
                "last_name": "Новикова",
                "first_name": "Елена",
                "phone": "+79001112277",
                "email": "novikova@example.com",
                "ad": ads[0],
                "status": Lead.Status.NEW,
            },
        ]
        leads = []
        for l in leads_data:
            lead, created = Lead.objects.get_or_create(
                phone=l["phone"],
                defaults={
                    "last_name": l["last_name"],
                    "first_name": l["first_name"],
                    "email": l["email"],
                    "ad": l["ad"],
                    "status": l["status"],
                },
            )
            if not created and lead.status != l["status"]:
                lead.status = l["status"]
                lead.save(update_fields=["status"])
            leads.append(lead)
            self.stdout.write(
                f"Лид '{lead}': {'создан' if created else 'уже существует'}"
            )

        # 4. Контракты (2 шт.)
        contracts_data = [
            {
                "name": "Контракт на контекстную рекламу",
                "product": products[0],
                "start_date": timezone.now().date(),
                "end_date": timezone.now().date() + timezone.timedelta(days=30),
                "cost": Decimal("60000.00"),
            },
            {
                "name": "Контракт на SMM",
                "product": products[1],
                "start_date": timezone.now().date(),
                "end_date": timezone.now().date() + timezone.timedelta(days=60),
                "cost": Decimal("90000.00"),
            },
        ]
        contracts = []
        for c in contracts_data:
            filename = f"contract_{c['name'].split()[0]}.txt"
            file_content = "Договор о предоставлении услуг".encode("utf-8")

            contract, created = Contract.objects.get_or_create(
                name=c["name"],
                defaults={
                    "product": c["product"],
                    "start_date": c["start_date"],
                    "end_date": c["end_date"],
                    "cost": c["cost"],
                },
            )
            if created:
                contract.file.save(filename, ContentFile(file_content), save=True)
            contracts.append(contract)
            self.stdout.write(
                f"Контракт '{contract.name}': {'создан' if created else 'уже существует'}"
            )

        # 5. Активные клиенты (2 шт., созданы из лидов)
        customers_data = [
            {"lead": leads[0], "contract": contracts[0]},
            {"lead": leads[2], "contract": contracts[1]},
        ]
        for cd in customers_data:
            customer, created = Customer.objects.get_or_create(
                lead=cd["lead"],
                defaults={"contract": cd["contract"]},
            )
            self.stdout.write(
                f"Клиент '{customer}': {'создан' if created else 'уже существует'}"
            )

        self.stdout.write(self.style.SUCCESS("Тестовые данные созданы"))
