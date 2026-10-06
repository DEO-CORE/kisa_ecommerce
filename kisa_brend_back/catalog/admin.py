from django.contrib import admin
from django.utils.html import format_html
from .models import Drop, Color, Size, Product, ProductColor, ProductImage, ProductSizeStock


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt', 'order')
    ordering = ('order',)


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('color', 'is_main', 'order')
    ordering = ('order',)


class ProductSizeStockInline(admin.TabularInline):
    model = ProductSizeStock
    extra = 0
    fields = ('color', 'size', 'quantity', 'reserved', 'available_display')
    readonly_fields = ('available_display',)
    ordering = ('color__order', 'size__order')
    verbose_name = 'Остаток по размеру'
    verbose_name_plural = 'Остатки по размерам (XS–XL)'

    def available_display(self, obj):
        if obj.pk:
            available = obj.available
            if available <= 0:
                return format_html('<span style="color: red;">Нет в наличии</span>')
            elif available <= 5:
                return format_html('<span style="color: orange;">{} шт. (мало)</span>', available)
            return format_html('<span style="color: green;">{} шт.</span>', available)
        return '-'
    available_display.short_description = 'Доступно'


@admin.register(Drop)
class DropAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order', 'products_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Товаров'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'hex_code', 'color_preview', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.hex_code
        )
    color_preview.short_description = 'Цвет'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'drop', 'price_rub', 'price_kgs', 'is_active', 'is_new', 'is_bestseller', 'total_stock', 'order')
    list_filter = ('drop', 'is_active', 'is_new', 'is_bestseller')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_new', 'is_bestseller', 'order')
    inlines = [ProductColorInline, ProductImageInline, ProductSizeStockInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'drop', 'main_image')
        }),
        ('Цены', {
            'fields': ('price_rub', 'price_kgs')
        }),
        ('Описание', {
            'fields': ('description', 'composition', 'fit_recommendation')
        }),
        ('Статус и порядок', {
            'fields': ('is_active', 'is_new', 'is_bestseller', 'order')
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

    def total_stock(self, obj):
        total = obj.get_total_stock()
        if total == 0:
            return format_html('<span style="color: red;">0</span>')
        elif total <= 10:
            return format_html('<span style="color: orange;">{}</span>', total)
        return total
    total_stock.short_description = 'Общий остаток'


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'is_main', 'order')
    list_filter = ('product__drop', 'color')
    list_editable = ('is_main', 'order')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'order')
    list_editable = ('order',)
    ordering = ('product', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'


@admin.register(ProductSizeStock)
class ProductSizeStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'quantity', 'reserved', 'available_display', 'is_low_stock', 'is_out_of_stock')
    list_filter = ('product__drop', 'color', 'size')
    search_fields = ('product__name',)
    list_editable = ('quantity', 'reserved')
    ordering = ('product', 'color', 'size__order')

    def available_display(self, obj):
        available = obj.available
        if available <= 0:
            return format_html('<span style="color: red;">Нет в наличии</span>')
        elif available <= 5:
            return format_html('<span style="color: orange;">{} шт. (мало)</span>', available)
        return format_html('<span style="color: green;">{} шт.</span>', available)
    available_display.short_description = 'Доступно'