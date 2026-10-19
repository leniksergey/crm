from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

ROLES = {
    "Оператор": [
        "leads.add_lead",
        "leads.change_lead",
        "leads.view_lead",
    ],
    "Маркетолог": [
        "products.add_product",
        "products.change_product",
        "products.view_product",
        "ads.add_advertisement",
        "ads.change_advertisement",
        "ads.view_advertisement",
    ],
    "Менеджер": [
        "contracts.add_contract",
        "contracts.change_contract",
        "contracts.view_contract",
        "contracts.delete_contract",
        "leads.view_lead",
        "customers.add_customer",
        "customers.change_customer",
        "customers.view_customer",
        "customers.delete_customer",
    ],
}


class Command(BaseCommand):
    help = "Создаёт группы-роли и выдаёт им права"

    def handle(self, *args, **options):
        for role, codes in ROLES.items():
            group, _ = Group.objects.get_or_create(name=role)
            permissions = []
            for code in codes:
                app_label, codename = code.split(".")
                permissions.append(
                    Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                )
            group.permissions.set(permissions)
            self.stdout.write(f"{role}: {len(permissions)} прав")
