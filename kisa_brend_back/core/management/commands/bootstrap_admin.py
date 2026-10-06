"""Create the initial administrator from private deployment environment variables."""
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create the initial superuser once; never replace existing credentials.'

    def handle(self, *args, **options):
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        if not password:
            self.stdout.write('Administrator bootstrap is not configured; skipped.')
            return

        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
        User = get_user_model()
        existing = User.objects.filter(username=username).first()
        if existing:
            if not (existing.is_active and existing.is_staff and existing.is_superuser):
                raise CommandError('The bootstrap username belongs to a non-administrator.')
            self.stdout.write('Administrator already exists; credentials unchanged.')
            return

        candidate = User(username=username, email=email)
        try:
            validate_password(password, user=candidate)
        except ValidationError:
            # Do not echo the password or validator details into public build logs.
            raise CommandError('The initial administrator password does not meet password requirements.')

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write('Initial administrator created successfully.')
