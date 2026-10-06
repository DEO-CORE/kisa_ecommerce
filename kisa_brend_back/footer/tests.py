from importlib import import_module
from django.apps import apps
from django.db import connection
from django.test import TestCase
from .models import InfoPage


class InformationPageTests(TestCase):
    def test_seed_preserves_edited_and_inactive_documents(self):
        page = InfoPage.objects.get(page_type='privacy')
        page.content = 'Редакция владельца магазина'
        page.is_active = False
        page.save()
        migration = import_module('footer.migrations.0003_information_pages')
        migration.seed_pages(apps, connection.schema_editor(atomic=False))
        page.refresh_from_db()
        self.assertEqual(page.content, 'Редакция владельца магазина')
        self.assertFalse(page.is_active)

    def test_public_pages_exist_and_hidden_pages_are_not_exposed(self):
        for slug in ['privacy', 'cookies', 'terms', 'delivery', 'payment', 'returns', 'contacts', 'documents']:
            response = self.client.get(f'/api/footer/info-pages/{slug}/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()['content'])
        InfoPage.objects.filter(page_type='privacy').update(is_active=False)
        self.assertEqual(self.client.get('/api/footer/info-pages/privacy/').status_code, 404)
        listing = self.client.get('/api/footer/info-pages/').json()['results']
        self.assertNotIn('privacy', [page['page_type'] for page in listing])
