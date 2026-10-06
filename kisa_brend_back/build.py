"""Provision the production schema and shop media bucket before deployment."""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisa_shop.settings')
django.setup()
from django.conf import settings
from django.core.management import call_command
from django.db import connection

if os.getenv('VERCEL_ENV') == 'production':
    if connection.vendor != 'postgresql':
        raise RuntimeError('Production requires the connected PostgreSQL database.')
    with connection.cursor() as cursor:
        cursor.execute('CREATE SCHEMA IF NOT EXISTS kisa')
    call_command('migrate', interactive=False)
    from core.storage import SupabaseMediaStorage
    storage = SupabaseMediaStorage()
    storage.ensure_bucket()
    # Verify both authenticated uploads and public asset delivery on every release.
    import base64
    from urllib.request import urlopen
    from django.core.files.base import ContentFile
    probe = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a5XkAAAAASUVORK5CYII=')
    name = storage.save('_checks/deployment.png', ContentFile(probe))
    try:
        with urlopen(storage.url(name), timeout=30) as response:
            if response.read() != probe:
                raise RuntimeError('Persistent storage verification failed.')
    finally:
        storage.delete(name)
    print('Production database and persistent media storage ready.')
