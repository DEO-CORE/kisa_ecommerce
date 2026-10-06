from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Contacts, Partnership, Support, InfoPage, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Цвета сайта', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
    )


@admin.register(Contacts)
class ContactsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Контакты', {
            'fields': ('telegram_url', 'phone', 'address', 'work_hours')
        }),
    )


@admin.register(Partnership)
class PartnershipAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Сотрудничество', {
            'fields': ('email', 'description')
        }),
    )


@admin.register(Support)
class SupportAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Поддержка', {
            'fields': ('telegram_url', 'email', 'description')
        }),
    )


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('page_type', 'title', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    list_filter = ('page_type', 'is_active')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('page_type', 'title', 'content', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )