from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Product, Color, Size, ProductColor, ProductSizeStock
from orders.models import Order


class CheckoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='Худи', slug='hoodie', price_kgs=2500, price_rub=2000)
        self.color = Color.objects.create(name='Чёрный', slug='black')
        self.size = Size.objects.create(name='M')
        ProductColor.objects.create(product=self.product, color=self.color)
        self.stock = ProductSizeStock.objects.create(product=self.product, color=self.color, size=self.size, quantity=3)
        self.item = dict(product_id=self.product.pk, color_id=self.color.pk, size_name='M', quantity=2)

    def checkout(self, items):
        return self.client.post('/api/orders/', dict(customer_name='Тест', customer_phone='+996555123456', currency='KGS', items=items), format='json')

    def test_server_prices_number_and_reservation(self):
        response = self.checkout([{**self.item, 'price_kgs': 1}])
        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(response.data['order_number'].startswith('KISA-'))
        order = Order.objects.get()
        self.assertEqual(order.total, Decimal('5000'))
        self.assertEqual(order.items.get().product_id, self.product.pk)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.reserved, 2)

    def test_duplicate_rows_cannot_oversell(self):
        response = self.checkout([self.item, self.item])
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Order.objects.exists())
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.reserved, 0)

    def test_empty_order_rejected(self):
        self.assertEqual(self.checkout([]).status_code, 400)

    def test_catalog_detail_color_shape(self):
        response = self.client.get('/api/catalog/products/hoodie/')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['colors'][0]['color']['id'], self.color.pk)
        self.assertEqual(response.data['stocks'][0]['available'], 3)

    def test_cancel_releases_reservation_once(self):
        from orders.services import transition_order
        self.checkout([self.item])
        order = Order.objects.get()
        transition_order(order.pk, 'CANCELLED')
        transition_order(order.pk, 'CANCELLED')
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.reserved, 0)
        self.assertEqual(self.stock.quantity, 3)

    def test_shipment_and_return_update_stock_once(self):
        from orders.services import transition_order
        self.checkout([self.item])
        order = Order.objects.get()
        for status in ['PAID', 'SHIPPED', 'SHIPPED', 'DELIVERED', 'RETURNED', 'RETURNED']:
            transition_order(order.pk, status)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.reserved, 0)
        self.assertEqual(self.stock.quantity, 3)
