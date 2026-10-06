"""Persistent public shop assets backed by the connected Supabase project."""
import json
import mimetypes
import uuid
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class SupabaseMediaStorage(Storage):
    def __init__(self):
        self.base = settings.SUPABASE_URL.rstrip('/') + '/storage/v1'
        self.bucket = settings.SUPABASE_MEDIA_BUCKET
        self.key = settings.SUPABASE_STORAGE_KEY

    def request(self, path, method='GET', data=None, content_type='application/json'):
        req = Request(self.base + path, data=data, method=method, headers={
            'Authorization': f'Bearer {self.key}', 'apikey': self.key,
            'Content-Type': content_type,
        })
        try:
            with urlopen(req, timeout=30) as response:
                return response.read()
        except HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError('Файл не найден в хранилище.') from None
            raise OSError(f'Хранилище вернуло ошибку {exc.code}.') from None

    def _save(self, name, content):
        directory, _, filename = name.rpartition('/')
        stem, dot, extension = filename.rpartition('.')
        suffix = f'.{extension}' if dot else ''
        name = '/'.join(filter(None, [directory, uuid.uuid4().hex + suffix]))
        payload = content.read()
        if len(payload) > settings.FILE_UPLOAD_MAX_BYTES:
            raise OSError('Файл превышает допустимый размер загрузки.')
        self.request(f'/object/{quote(self.bucket)}/{quote(name, safe="/")}',
                     method='POST', data=payload,
                     content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
        return name

    def _open(self, name, mode='rb'):
        return ContentFile(self.request(f'/object/{quote(self.bucket)}/{quote(name, safe="/")}'), name=name)

    def exists(self, name):
        # Uploaded names are random and never overwrite existing objects.
        return False

    def url(self, name):
        return f'{self.base}/object/public/{quote(self.bucket)}/{quote(name, safe="/")}'

    def delete(self, name):
        self.request(f'/object/{quote(self.bucket)}', method='DELETE',
                     data=json.dumps({'prefixes': [name]}).encode())

    def size(self, name):
        info = json.loads(self.request(f'/object/info/{quote(self.bucket)}/{quote(name, safe="/")}'))
        return int(info.get('metadata', {}).get('size', 0))

    def ensure_bucket(self):
        # Do not alter permissions of a pre-existing bucket.
        buckets = json.loads(self.request('/bucket'))
        existing = next((item for item in buckets if item['id'] == self.bucket), None)
        if existing:
            if not existing.get('public'):
                raise OSError('Для фотографий магазина нужен отдельный публичный bucket.')
            return
        self.request('/bucket', method='POST', data=json.dumps({
            'id': self.bucket, 'name': self.bucket, 'public': True,
            'file_size_limit': settings.FILE_UPLOAD_MAX_BYTES,
            'allowed_mime_types': ['image/*', 'video/mp4', 'video/webm'],
        }).encode())
