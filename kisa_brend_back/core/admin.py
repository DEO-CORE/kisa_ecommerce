from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SingletonBase, TimeStampedModel, SEOModel


admin.site.site_header = 'KISA Shop — Админ-панель'
admin.site.site_title = 'KISA Shop'
admin.site.index_title = 'Управление магазином'
admin.site.index_template = 'admin/kisa_index.html'
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
