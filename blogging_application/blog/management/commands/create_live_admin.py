import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the live admin account"

    def handle(self, *args, **options):
        username = os.environ.get("LIVE_ADMIN_USERNAME")
        password = os.environ.get("LIVE_ADMIN_PASSWORD")
        email = os.environ.get("LIVE_ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "LIVE_ADMIN_USERNAME or LIVE_ADMIN_PASSWORD is missing."
                )
            )
            return

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Live admin created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS("Live admin updated successfully."))