from django.contrib import admin
from django import forms
from .services import transition_order, validate_transition
from django.utils.html import format_html
from .models import Order, OrderItem, OrderStatus


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean_status(self):
        status = self.cleaned_data['status']
        if self.instance.pk:
            validate_transition(Order.objects.get(pk=self.instance.pk).status, status)
        return status


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'color_name', 'size_name', 'quantity', 'price_rub', 'price_kgs', 'total_rub', 'total_kgs')
    fields = ('product_name', 'color_name', 'size_name', 'quantity', 'price_rub', 'price_kgs', 'total_rub', 'total_kgs')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        transition_order(obj.pk, obj.status)
        super().save_model(request, obj, form, change)

    list_display = ('order_number', 'customer_name', 'customer_phone', 'status', 'status_badge', 'total_display', 'currency', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_phone', 'customer_email')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'delivery_cost', 'total')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Заказ', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Клиент', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Доставка', {
            'fields': ('delivery_address', 'delivery_method', 'delivery_cost')
        }),
        ('Суммы', {
            'fields': ('subtotal', 'total', 'currency')
        }),
        ('Оплата', {
            'fields': ('payment_method', 'payment_id', 'paid_at')
        }),
        ('Примечания', {
            'fields': ('manager_notes', 'customer_notes'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            OrderStatus.NEW: '#3b82f6',
            OrderStatus.PAID: '#10b981',
            OrderStatus.SHIPPED: '#f59e0b',
            OrderStatus.DELIVERED: '#8b5cf6',
            OrderStatus.COMPLETED: '#059669',
            OrderStatus.CANCELLED: '#ef4444',
            OrderStatus.RETURNED: '#f97316',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 10px; border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

    def total_display(self, obj):
        symbol = '₽' if obj.currency == 'RUB' else 'сом'
        return f'{obj.total} {symbol}'
    total_display.short_description = 'Итого'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'color_name', 'size_name', 'quantity', 'price_rub', 'total_rub')
    list_filter = ('order__status',)
    search_fields = ('order__order_number', 'product_name')
    readonly_fields = ('order', 'product_name', 'color_name', 'size_name', 'quantity', 'price_rub', 'price_kgs', 'total_rub', 'total_kgs')