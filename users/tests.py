from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase

from ads.models import Advertisement
from leads.models import Lead
from products.models import Product

User = get_user_model()
PASSWORD = "pass12345"

# (роль, адрес, ожидаемый код): 302 = отправили на вход, 403 = доступ закрыт
CASES = [
    (None, "/", 302),
    (None, "/leads/", 302),
    (None, "/ads/statistic", 302),
    ("Оператор", "/leads/", 200),
    ("Оператор", "/leads/new", 200),
    ("Оператор", "/leads/1/delete", 200),
    ("Оператор", "/products/", 403),
    ("Оператор", "/ads/", 403),
    ("Оператор", "/contracts/", 403),
    ("Оператор", "/customers/", 403),
    ("Оператор", "/ads/statistic", 200),
    ("Маркетолог", "/products/", 200),
    ("Маркетолог", "/products/new", 200),
    ("Маркетолог", "/ads/", 200),
    ("Маркетолог", "/ads/new", 200),
    ("Маркетолог", "/products/1/delete", 200),
    ("Маркетолог", "/ads/1/delete", 200),
    ("Маркетолог", "/leads/", 403),
    ("Маркетолог", "/contracts/", 403),
    ("Маркетолог", "/customers/", 403),
    ("Маркетолог", "/ads/statistic", 200),
    ("Менеджер", "/contracts/", 200),
    ("Менеджер", "/contracts/new", 200),
    ("Менеджер", "/leads/", 200),
    ("Менеджер", "/leads/new", 403),
    ("Менеджер", "/customers/", 200),
    ("Менеджер", "/customers/new", 200),
    ("Менеджер", "/products/", 403),
    ("Менеджер", "/ads/", 403),
    ("Менеджер", "/ads/statistic", 200),
]


class RoleAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_roles", verbosity=0)
        product = Product.objects.create(name="Услуга", cost=Decimal("1000.00"))
        advertisement = Advertisement.objects.create(
            name="Кампания",
            product=product,
            channel="VK",
            budget=Decimal("5000.00"),
        )
        Lead.objects.create(
            last_name="Иванов",
            first_name="Иван",
            phone="+79000000001",
            email="ivanov@example.com",
            ad=advertisement,
        )
        for group in Group.objects.all():
            user = User.objects.create_user(username=group.name, password=PASSWORD)
            user.groups.add(group)

    def test_access_matrix(self):
        for role, url, expected in CASES:
            with self.subTest(role=role, url=url):
                self.client.logout()
                if role:
                    self.client.login(username=role, password=PASSWORD)
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected)

    def test_manager_cannot_see_lead_editing_actions(self):
        self.client.login(username="Менеджер", password=PASSWORD)

        response = self.client.get("/leads/1/")

        self.assertNotContains(response, "Редактировать")
        self.assertNotContains(response, "Удалить")
