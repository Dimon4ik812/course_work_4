import json

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда для создание фикстуры групп пользователей"""

    def handle(self, *args, **options):
        groups = Group.objects.all()
        group_data = []

        for group in groups:
            group_data.append(
                {
                    "id": group.id,
                    "name": group.name,
                    "permissions": [perm.codename for perm in group.permissions.all()],
                }
            )

        with open("group_fixture.json", "w") as f:
            json.dump(group_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS("Файл group_fixture.json успешно создан"))
