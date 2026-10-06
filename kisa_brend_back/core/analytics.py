from datetime import datetime, time, timedelta

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.utils import timezone

from orders.models import Order, OrderItem, OrderStatus

REVENUE_STATUSES = [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.COMPLETED]


@staff_member_required
def analytics(request):
    if not request.user.has_perms(['orders.view_order', 'orders.view_orderitem']):
        raise PermissionDenied
    days = request.GET.get('days', '30')
    days = int(days) if days in {'7', '30', '90'} else 30
    today = timezone.localdate()
    start_day = today - timedelta(days=days - 1)
    start = timezone.make_aware(datetime.combine(start_day, time.min))
    end = timezone.make_aware(datetime.combine(today + timedelta(days=1), time.min))
    orders = Order.objects.filter(created_at__gte=start, created_at__lt=end)
    paid = orders.filter(status__in=REVENUE_STATUSES)
    totals = list(paid.order_by().values('currency').annotate(revenue=Sum('total'), average=Avg('total'), count=Count('pk')).order_by('currency'))
    daily_counts = {row['day']: row['count'] for row in orders.order_by().annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('pk'))}
    peak = max(daily_counts.values(), default=1) or 1
    daily = [{'date': start_day + timedelta(days=offset), 'count': daily_counts.get(start_day + timedelta(days=offset), 0)} for offset in range(days)]
    for row in daily:
        row['width'] = round(row['count'] / peak * 100)
    statuses = {row['status']: row['count'] for row in orders.order_by().values('status').annotate(count=Count('pk'))}
    context = {
        **admin.site.each_context(request),
        'title': 'Аналитика магазина', 'days': days, 'start_day': start_day, 'today': today,
        'total_orders': orders.count(), 'new_orders': statuses.get(OrderStatus.NEW, 0),
        'paid_orders': paid.count(), 'revenue_totals': totals,
        'daily': daily, 'statuses': [{'label': label, 'count': statuses.get(value, 0)} for value, label in OrderStatus.choices],
        'top_products': OrderItem.objects.filter(order__in=paid).order_by().values('product_name', 'product_sku').annotate(quantity=Sum('quantity')).order_by('-quantity', 'product_name')[:10],
    }
    return TemplateResponse(request, 'admin/kisa_analytics.html', context)
