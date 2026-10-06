from django.core.exceptions import ValidationError
from django.db import transaction
from catalog.models import ProductSizeStock
from .models import Order

TRANSITIONS = {
    'NEW': {'PAID', 'CANCELLED'}, 'PAID': {'SHIPPED', 'CANCELLED'},
    'SHIPPED': {'DELIVERED'}, 'DELIVERED': {'COMPLETED', 'RETURNED'},
    'COMPLETED': {'RETURNED'},
}


def validate_transition(old_status, new_status):
    if old_status != new_status and new_status not in TRANSITIONS.get(old_status, set()):
        raise ValidationError('Недопустимый переход статуса заказа.')


@transaction.atomic
def transition_order(order_id, new_status):
    order = Order.objects.select_for_update().get(pk=order_id)
    validate_transition(order.status, new_status)
    if order.status == new_status:
        return order
    if new_status in {'CANCELLED', 'SHIPPED', 'RETURNED'}:
        for item in order.items.order_by('product_id', 'color_id', 'size_id'):
            try:
                stock = ProductSizeStock.objects.select_for_update().get(
                    product=item.product, color=item.color, size=item.size)
            except ProductSizeStock.DoesNotExist:
                raise ValidationError('Остаток товара удалён. Восстановите его перед изменением статуса.')
            if new_status == 'CANCELLED':
                stock.reserved = max(0, stock.reserved - item.quantity)
            elif new_status == 'SHIPPED':
                if stock.quantity < item.quantity:
                    raise ValidationError('Недостаточно товара для отгрузки.')
                stock.quantity -= item.quantity
                stock.reserved = max(0, stock.reserved - item.quantity)
            else:
                stock.quantity += item.quantity
            stock.save()
    order.status = new_status
    order.save(update_fields=['status', 'updated_at'])
    return order
