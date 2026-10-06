from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id):
    from orders.models import Order
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Подтверждение заказа #{order.order_number}'
        message = f'''
        Здравствуйте, {order.customer_name}!
        
        Ваш заказ #{order.order_number} успешно оформлен.
        Сумма: {order.total} {order.currency}
        
        Спасибо за покупку в KISA!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer_email],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        pass
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_order_status_change_email(self, order_id, old_status, new_status):
    from orders.models import Order, OrderStatus
    try:
        order = Order.objects.get(id=order_id)
        status_labels = dict(OrderStatus.choices)
        subject = f'Изменение статуса заказа #{order.order_number}'
        message = f'''
        Здравствуйте, {order.customer_name}!
        
        Статус вашего заказа #{order.order_number} изменен:
        {status_labels.get(old_status, old_status)} → {status_labels.get(new_status, new_status)}
        
        Команда KISA
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.customer_email],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        pass
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task
def reserve_stock_for_order(order_id):
    from orders.models import Order
    from catalog.models import ProductSizeStock
    from django.db import transaction
    
    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order_id)
            for item in order.items.all():
                stock = ProductSizeStock.objects.select_for_update().get(
                    product=item.product,
                    color__name=item.color_name,
                    size__name=item.size_name
                )
                if stock.available < item.quantity:
                    raise ValueError(f'Недостаточно товара: {item.product_name} ({item.color_name}, {item.size_name})')
                stock.reserved += item.quantity
                stock.save()
    except (Order.DoesNotExist, ProductSizeStock.DoesNotExist, ValueError) as e:
        return {'success': False, 'error': str(e)}
    return {'success': True}


@shared_task
def release_reserved_stock(order_id):
    from orders.models import Order
    from catalog.models import ProductSizeStock
    from django.db import transaction
    
    try:
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            for item in order.items.all():
                stock = ProductSizeStock.objects.select_for_update().get(
                    product=item.product,
                    color__name=item.color_name,
                    size__name=item.size_name
                )
                stock.reserved = max(0, stock.reserved - item.quantity)
                stock.save()
    except (Order.DoesNotExist, ProductSizeStock.DoesNotExist):
        pass
    return {'success': True}


@shared_task
def confirm_stock_reservation(order_id):
    from orders.models import Order
    from catalog.models import ProductSizeStock
    from django.db import transaction
    
    try:
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            for item in order.items.all():
                stock = ProductSizeStock.objects.select_for_update().get(
                    product=item.product,
                    color__name=item.color_name,
                    size__name=item.size_name
                )
                stock.quantity -= item.quantity
                stock.reserved = max(0, stock.reserved - item.quantity)
                stock.save()
    except (Order.DoesNotExist, ProductSizeStock.DoesNotExist):
        pass
    return {'success': True}