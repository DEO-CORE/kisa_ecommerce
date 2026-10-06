from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from catalog.models import Product, Color, Size


class OrderStatus(models.TextChoices):
    NEW = 'NEW', 'Новый'
    PAID = 'PAID', 'Оплачен'
    SHIPPED = 'SHIPPED', 'Отправлен'
    DELIVERED = 'DELIVERED', 'Доставлен'
    COMPLETED = 'COMPLETED', 'Завершен'
    CANCELLED = 'CANCELLED', 'Отменен'
    RETURNED = 'RETURNED', 'Возврат'


class Order(TimeStampedModel):
    order_number = models.CharField('Номер заказа', max_length=20, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Пользователь'
    )
    status = models.CharField('Статус', max_length=20, choices=OrderStatus.choices, default=OrderStatus.NEW)
    
    # Customer info
    customer_name = models.CharField('Имя клиента', max_length=100)
    customer_phone = models.CharField('Телефон', max_length=20)
    customer_email = models.EmailField('Email', blank=True)
    
    # Delivery
    delivery_address = models.TextField('Адрес доставки', blank=True)
    delivery_method = models.CharField('Способ доставки', max_length=100, blank=True)
    delivery_cost = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=2, default=0)
    
    # Totals
    subtotal = models.DecimalField('Сумма товаров', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)
    currency = models.CharField('Валюта', max_length=3, default='RUB')
    
    # Payment
    payment_method = models.CharField('Способ оплаты', max_length=50, blank=True)
    payment_id = models.CharField('ID платежа', max_length=100, blank=True)
    paid_at = models.DateTimeField('Оплачено', null=True, blank=True)
    
    # Notes
    manager_notes = models.TextField('Примечания менеджера', blank=True)
    customer_notes = models.TextField('Примечания клиента', blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.order_number} — {self.customer_name}'

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='order_items')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, related_name='order_items')
    
    # Snapshot of product data at time of order
    product_name = models.CharField('Название товара', max_length=200)
    product_sku = models.CharField('Артикул', max_length=50, blank=True)
    color_name = models.CharField('Цвет', max_length=50)
    size_name = models.CharField('Размер', max_length=10)
    
    quantity = models.PositiveIntegerField('Количество', default=1)
    price_rub = models.DecimalField('Цена (₽)', max_digits=10, decimal_places=2)
    price_kgs = models.DecimalField('Цена (сом)', max_digits=10, decimal_places=2, default=0)
    total_rub = models.DecimalField('Сумма (₽)', max_digits=10, decimal_places=2)
    total_kgs = models.DecimalField('Сумма (сом)', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product_name} ({self.color_name}, {self.size_name}) × {self.quantity}'

    def save(self, *args, **kwargs):
        if not self.total_rub:
            self.total_rub = self.price_rub * self.quantity
        if not self.total_kgs:
            self.total_kgs = self.price_kgs * self.quantity
        super().save(*args, **kwargs)