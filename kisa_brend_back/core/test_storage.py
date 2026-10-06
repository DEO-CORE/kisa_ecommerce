import json
from unittest.mock import patch
from django.test import SimpleTestCase, override_settings
from django.core.files.base import ContentFile
from .storage import SupabaseMediaStorage


@override_settings(SUPABASE_URL='https://example.supabase.co', SUPABASE_MEDIA_BUCKET='kisa-media',
                   SUPABASE_STORAGE_KEY='server-secret', FILE_UPLOAD_MAX_BYTES=1024)
class StorageTests(SimpleTestCase):
    def test_upload_uses_unique_name_and_public_asset_url(self):
        storage = SupabaseMediaStorage()
        with patch.object(storage, 'request', return_value=b'{}') as request:
            name = storage.save('products/photo.png', ContentFile(b'image'))
            self.assertTrue(name.startswith('products/'))
            self.assertTrue(name.endswith('.png'))
            self.assertNotEqual(name, 'products/photo.png')
            self.assertEqual(request.call_args.kwargs['data'], b'image')
            self.assertIn('/object/public/kisa-media/products/', storage.url(name))
            self.assertNotIn('server-secret', storage.url(name))

    def test_existing_bucket_permissions_are_preserved(self):
        storage = SupabaseMediaStorage()
        with patch.object(storage, 'request', return_value=json.dumps([{'id': 'kisa-media', 'public': True}]).encode()) as request:
            storage.ensure_bucket()
            request.assert_called_once_with('/bucket')

    def test_private_bucket_is_not_made_public(self):
        storage = SupabaseMediaStorage()
        with patch.object(storage, 'request', return_value=json.dumps([{'id': 'kisa-media', 'public': False}]).encode()) as request:
            with self.assertRaises(OSError):
                storage.ensure_bucket()
            request.assert_called_once_with('/bucket')

    def test_oversized_upload_is_rejected_before_request(self):
        storage = SupabaseMediaStorage()
        with patch.object(storage, 'request') as request:
            with self.assertRaises(OSError):
                storage.save('photo.png', ContentFile(b'x' * 1025))
            request.assert_not_called()
