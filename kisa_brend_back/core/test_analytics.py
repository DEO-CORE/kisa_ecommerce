from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from orders.models import Order, OrderItem


class AnalyticsTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(username='report-admin', password='test-password')

    def order(self, number, status='PAID', currency='RUB', total='100'):
        return Order.objects.create(order_number=number, status=status, currency=currency, total=total, customer_name='Test', customer_phone='123')

    def test_access_requires_staff_and_order_permissions(self):
        self.assertEqual(self.client.get('/admin/analytics/').status_code, 302)
        staff = get_user_model().objects.create_user(username='limited', is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get('/admin/analytics/').status_code, 403)

    def test_totals_exclude_returns_and_cancellations_and_keep_currencies_separate(self):
        self.order('1', total='100')
        self.order('2', status='COMPLETED', total='300')
        self.order('3', currency='KGS', total='500')
        self.order('4', status='RETURNED', total='900')
        self.order('5', status='CANCELLED', total='900')
        self.order('6', status='NEW', total='900')
        old = self.order('7', total='700')
        Order.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=100))
        self.client.force_login(self.admin)
        response = self.client.get('/admin/analytics/?days=7')
        self.assertEqual(response.status_code, 200)
        self.assertIn('no-store', response.headers['Cache-Control'])
        self.assertEqual(response.context['total_orders'], 6)
        self.assertEqual(response.context['paid_orders'], 3)
        totals = {row['currency']: row for row in response.context['revenue_totals']}
        self.assertEqual(totals['RUB']['revenue'], Decimal('400'))
        self.assertEqual(totals['RUB']['average'], Decimal('200'))
        self.assertEqual(totals['KGS']['revenue'], Decimal('500'))
        self.assertEqual(sum(row['count'] for row in response.context['daily']), 6)

    def test_top_products_use_paid_quantity_only_and_invalid_period_falls_back(self):
        paid = self.order('1')
        returned = self.order('2', status='RETURNED')
        for order, quantity in [(paid, 2), (returned, 10)]:
            OrderItem.objects.create(order=order, product_name='Худи', color_name='Белый', size_name='M', quantity=quantity, price_rub=100, total_rub=100 * quantity)
        self.client.force_login(self.admin)
        response = self.client.get('/admin/analytics/?days=99999')
        self.assertEqual(response.context['days'], 30)
        self.assertEqual(list(response.context['top_products'])[0]['quantity'], 2)

    def test_empty_dashboard_renders(self):
        self.client.force_login(self.admin)
        response = self.client.get('/admin/analytics/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Данных о продажах пока нет')
        self.assertEqual(response.context['total_orders'], 0)
        self.assertContains(self.client.get('/admin/'), '/admin/analytics/')
