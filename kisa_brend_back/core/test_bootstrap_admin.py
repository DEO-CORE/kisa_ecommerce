from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class BootstrapAdminTests(TestCase):
    def run_bootstrap(self, **environment):
        output = StringIO()
        with patch.dict('os.environ', environment, clear=True):
            call_command('bootstrap_admin', stdout=output)
        return output.getvalue()

    def test_creates_admin_once_without_changing_password(self):
        first = 'A-strong-initial-password-2947'
        output = self.run_bootstrap(DJANGO_SUPERUSER_PASSWORD=first)
        self.run_bootstrap(DJANGO_SUPERUSER_PASSWORD='A-different-password-3948')
        user = get_user_model().objects.get(username='admin')
        self.assertTrue(user.is_active and user.is_staff and user.is_superuser)
        self.assertTrue(user.check_password(first))
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertNotIn(first, output)

    def test_no_password_does_not_create_an_account(self):
        self.run_bootstrap()
        self.assertFalse(get_user_model().objects.exists())

    def test_existing_regular_user_is_not_promoted(self):
        user = get_user_model().objects.create_user(username='admin', password='original')
        with self.assertRaises(CommandError):
            self.run_bootstrap(DJANGO_SUPERUSER_PASSWORD='A-strong-password-4839')
        user.refresh_from_db()
        self.assertFalse(user.is_superuser or user.is_staff)
        self.assertTrue(user.check_password('original'))

    def test_weak_password_is_rejected_without_creating_account(self):
        with self.assertRaises(CommandError):
            self.run_bootstrap(DJANGO_SUPERUSER_PASSWORD='123')
        self.assertFalse(get_user_model().objects.exists())
