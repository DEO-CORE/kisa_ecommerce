"""
Django settings for kisa_shop project.
"""

from pathlib import Path
import os
import hashlib
import hmac
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

IS_VERCEL = os.getenv('VERCEL') == '1'
_secret_source = os.getenv('SUPABASE_SECRET_KEY') or os.getenv('SUPABASE_SERVICE_ROLE_KEY')
_secret_default = (hmac.new(_secret_source.encode(), b'kisa-django-signing-v1', hashlib.sha256).hexdigest()
                   if IS_VERCEL and _secret_source else 'django-insecure-dev-key-change-in-production')
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') or _secret_default

DEBUG = os.getenv('DEBUG', 'False' if IS_VERCEL else 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,kisa.deo-core.codes,kisa.backend.deo-core.codes,kisa-ecommerce-back.vercel.app').split(',')
if IS_VERCEL and os.getenv('VERCEL_URL'):
    ALLOWED_HOSTS.append(os.environ['VERCEL_URL'])

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'django_filters',
    'mptt',
    'colorfield',
    'solo',
    'drf_spectacular',
    
    # Local apps
    'core',
    'catalog',
    'about',
    'journal',
    'orders',
    'footer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kisa_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kisa_shop.wsgi.application'

import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
if DATABASE_URL:
    # Marketplace URLs may contain client metadata that libpq does not accept.
    parts = urlsplit(DATABASE_URL)
    query = [(key, value) for key, value in parse_qsl(parts.query) if key not in {'supa', 'pgbouncer', 'connection_limit', 'pool_timeout'}]
    DATABASE_URL = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=0 if IS_VERCEL else 600, conn_health_checks=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

if IS_VERCEL:
    if not DATABASE_URL:
        raise ValueError('Connect a PostgreSQL database before deploying.')
    DATABASES['default'].setdefault('OPTIONS', {})['options'] = '-c search_path=kisa,public'
    DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_title': 'KISA Shop',
    'site_header': 'KISA Shop',
    'site_brand': 'KISA',
    'welcome_sign': 'Управление магазином KISA',
    'copyright': 'KISA',
    'show_ui_builder': False,
    'topmenu_links': [{'name': 'Аналитика', 'url': 'admin-analytics', 'permissions': ['orders.view_order', 'orders.view_orderitem']}],
    'navigation_expanded': True,
    'order_with_respect_to': ['catalog', 'orders', 'about', 'journal', 'footer', 'core', 'auth'],
    'icons': {
        'catalog': 'fas fa-tshirt',
        'orders': 'fas fa-shopping-bag',
        'about': 'fas fa-info-circle',
        'journal': 'fas fa-newspaper',
        'footer': 'fas fa-cog',
        'core': 'fas fa-envelope',
        'auth': 'fas fa-users-cog',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'KISA Shop API',
    'DESCRIPTION': 'API для интернет-магазина женской одежды KISA',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'TAGS': [
        {'name': 'catalog', 'description': 'Каталог товаров: дропы, продукты, цвета, размеры, остатки'},
        {'name': 'about', 'description': 'О бренде: главная, принципы, история, команда'},
        {'name': 'journal', 'description': 'Журнал/Новости: публикации, статьи'},
        {'name': 'orders', 'description': 'Заказы: создание, просмотр, изменение статуса'},
        {'name': 'footer', 'description': 'Футер: контакты, сотрудничество, поддержка, настройки цветов'},
    ],
}

# Redis & Celery
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Email
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@kisa.shop')

# Solo (Singleton) settings
SOLO_CACHE = 'default'
SOLO_CACHE_TIMEOUT = 300

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}
# TLS terminates at the deployment proxy. Backend ports are private.
CSRF_TRUSTED_ORIGINS = [v for v in os.getenv('CSRF_TRUSTED_ORIGINS', 'https://kisa.deo-core.codes,https://kisa.backend.deo-core.codes,https://kisa-ecommerce-back.vercel.app').split(',') if v]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
if not DEBUG and SECRET_KEY == 'django-insecure-dev-key-change-in-production':
    raise ValueError('DJANGO_SECRET_KEY must be set in production')
if os.getenv('CACHE_BACKEND') == 'local' or (IS_VERCEL and not os.getenv('REDIS_URL')):
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

if IS_VERCEL:
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_STORAGE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_SECRET_KEY', '')
    SUPABASE_MEDIA_BUCKET = os.getenv('SUPABASE_MEDIA_BUCKET', 'kisa-media')
    FILE_UPLOAD_MAX_BYTES = 50 * 1024 * 1024
    FILE_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024
    FILE_UPLOAD_TEMP_DIR = '/tmp'
    if not SUPABASE_URL or not SUPABASE_STORAGE_KEY:
        raise ValueError('Connect Supabase Storage before deploying.')
    STORAGES = {
        'default': {'BACKEND': 'core.storage.SupabaseMediaStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }
