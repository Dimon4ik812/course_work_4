from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from config.settings import ADMIN_EMAIL, ADMIN_PASSWORD


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(email=ADMIN_EMAIL, first_name="admin", last_name="admin")

        user.set_password(ADMIN_PASSWORD)

        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user with email {user.email}!"))
