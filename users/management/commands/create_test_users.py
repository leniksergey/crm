from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand


USERS = [
    {
        "username": "operator",
        "password": "password123",
        "email": "operator@example.com",
        "first_name": "Иван",
        "last_name": "Иванов",
        "group": "Оператор",
    },
    {
        "username": "marketer",
        "password": "password123",
        "email": "marketer@example.com",
        "first_name": "Петр",
        "last_name": "Петров",
        "group": "Маркетолог",
    },
    {
        "username": "manager",
        "password": "password123",
        "email": "manager@example.com",
        "first_name": "Сергей",
        "last_name": "Сергеев",
        "group": "Менеджер",
    },
]


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей и назначает им группы-роли"

    def handle(self, *args, **options):
        for user_data in USERS:
            username = user_data["username"]
            password = user_data["password"]
            group_name = user_data["group"]

            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.email = user_data.get("email", "")
            user.first_name = user_data.get("first_name", "")
            user.last_name = user_data.get("last_name", "")
            user.save()

            try:
                group = Group.objects.get(name=group_name)
                user.groups.set([group])
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Группа '{group_name}' не найдена. "
                        f"Запустите python manage.py setup_roles."
                    )
                )

            action = "создан" if created else "обновлён"
            self.stdout.write(
                f"Пользователь {username}: {action}, группа '{group_name}'"
            )
