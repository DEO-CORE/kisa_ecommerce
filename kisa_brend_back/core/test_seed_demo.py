import tempfile
from io import StringIO
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase, override_settings
from catalog.models import Product, ProductColor, ProductSizeStock
from core.models import SeedRun
from journal.models import Publication


class DemoSeedTests(TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.storage = override_settings(MEDIA_ROOT=self.directory.name, STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'}})
        self.storage.enable()
        self.addCleanup(self.storage.disable)

    def seed(self):
        call_command('seed_demo', stdout=StringIO())

    def test_catalogue_and_photos_exist_and_rerun_keeps_changes_and_deletions(self):
        self.seed()
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(ProductColor.objects.count(), 9)
        self.assertEqual(ProductSizeStock.objects.count(), 45)
        self.assertEqual(Publication.objects.count(), 3)
        product = Product.objects.first()
        self.assertTrue(product.main_image.storage.exists(product.main_image.name))
        product.price_kgs = 123
        product.save()
        stock = product.stocks.first()
        stock.quantity, stock.reserved = 7, 2
        stock.save()
        deleted = Product.objects.last()
        deleted_slug = deleted.slug
        deleted.delete()
        self.seed()
        product.refresh_from_db()
        stock.refresh_from_db()
        self.assertEqual(product.price_kgs, 123)
        self.assertEqual((stock.quantity, stock.reserved), (7, 2))
        self.assertFalse(Product.objects.filter(slug=deleted_slug).exists())
        self.assertEqual(SeedRun.objects.count(), 1)

    def test_existing_product_is_not_modified(self):
        original = Product.objects.create(slug='demo-zip-hoodie', name='Мой товар', price_kgs=999)
        self.seed()
        original.refresh_from_db()
        self.assertEqual(original.name, 'Мой товар')
        self.assertEqual(original.price_kgs, 999)
        self.assertFalse(original.stocks.exists())

    def test_failed_upload_does_not_mark_seed_complete(self):
        with patch('core.management.commands.seed_demo.default_storage.save', side_effect=OSError('Upload failed')):
            with self.assertRaises(OSError):
                self.seed()
        self.assertFalse(SeedRun.objects.exists())
        self.assertFalse(Product.objects.exists())
        self.seed()
        self.assertEqual(Product.objects.count(), 3)
