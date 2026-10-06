from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import MainPageSettings, BrandPrinciple, BrandHistory, TeamBlock


@admin.register(MainPageSettings)
class MainPageSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Главный блок', {
            'fields': ('slogan', 'manifesto', 'team_photo', 'hero_video')
        }),
    )


@admin.register(BrandPrinciple)
class BrandPrincipleAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('number',)
    fieldsets = (
        (None, {
            'fields': ('number', 'title', 'description', 'icon', 'is_active')
        }),
    )


@admin.register(BrandHistory)
class BrandHistoryAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('-year',)
    fieldsets = (
        (None, {
            'fields': ('year', 'title', 'description', 'image', 'is_active')
        }),
    )


@admin.register(TeamBlock)
class TeamBlockAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Блок "Команда"', {
            'fields': ('text', 'photo')
        }),
    )