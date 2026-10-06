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
    SupabaseMediaStorage().ensure_bucket()
    print('Production database and persistent media storage ready.')
