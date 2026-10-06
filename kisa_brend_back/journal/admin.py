from django.contrib import admin
from django.utils.html import format_html
from .models import Publication, PublicationProduct


class PublicationProductInline(admin.TabularInline):
    model = PublicationProduct
    extra = 1
    fields = ('product', 'order', 'note')
    ordering = ('order',)
    autocomplete_fields = ('product',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_type_badge', 'published_at', 'is_published', 'is_featured', 'order', 'products_count')
    list_filter = ('pub_type', 'is_published', 'is_featured')
    search_fields = ('title', 'preview_text', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured', 'order')
    inlines = [PublicationProductInline]
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'published_at'
    ordering = ('-published_at', 'order')

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'pub_type', 'published_at', 'preview_image', 'hero_image')
        }),
        ('Контент', {
            'fields': ('preview_text', 'content')
        }),
        ('Статус и порядок', {
            'fields': ('is_published', 'is_featured', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def pub_type_badge(self, obj):
        colors = {
            'ITEM': '#6366f1',
            'PEOPLE': '#ec4899',
            'GUIDE': '#10b981',
            'EVENT': '#f59e0b',
        }
        color = colors.get(obj.pub_type, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_pub_type_display()
        )
    pub_type_badge.short_description = 'Тип'

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Товаров'


@admin.register(PublicationProduct)
class PublicationProductAdmin(admin.ModelAdmin):
    list_display = ('publication', 'product', 'order', 'note')
    list_editable = ('order',)
    autocomplete_fields = ('publication', 'product')