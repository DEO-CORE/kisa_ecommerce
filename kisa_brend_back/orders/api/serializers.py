from rest_framework import serializers
from orders.models import Order, OrderItem, OrderStatus


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_name', 'product_sku', 'color_name', 'size_name', 
                  'quantity', 'price_rub', 'price_kgs', 'total_rub', 'total_kgs')


class OrderListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'customer_name', 'customer_phone', 'status', 
                  'status_display', 'total', 'currency', 'items_count', 'created_at')
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'user', 'status', 'status_display',
                  'customer_name', 'customer_phone', 'customer_email',
                  'delivery_address', 'delivery_method', 'delivery_cost',
                  'subtotal', 'total', 'currency',
                  'payment_method', 'payment_id', 'paid_at',
                  'manager_notes', 'customer_notes',
                  'items', 'created_at', 'updated_at')


class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    color_id = serializers.IntegerField(min_value=1)
    size_name = serializers.CharField(max_length=10)
    quantity = serializers.IntegerField(min_value=1, max_value=100)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = CheckoutItemSerializer(many=True, allow_empty=False)
    currency = serializers.ChoiceField(choices=['KGS', 'RUB'], default='KGS')
    order_number = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('order_number', 'customer_name', 'customer_phone', 'customer_email',
                  'delivery_address', 'delivery_method', 'payment_method',
                  'currency', 'items', 'customer_notes')

    def create(self, validated_data):
        import uuid
        from decimal import Decimal
        from django.db import transaction
        from catalog.models import ProductSizeStock
        items = validated_data.pop('items')
        # Aggregate duplicate rows before checking stock, and lock in stable order.
        quantities = {}
        for item in items:
            key = (item['product_id'], item['color_id'], item['size_name'])
            quantities[key] = quantities.get(key, 0) + item['quantity']
        with transaction.atomic():
            rows = []
            for (product_id, color_id, size_name), quantity in sorted(quantities.items()):
                try:
                    stock = ProductSizeStock.objects.select_for_update().select_related(
                        'product', 'color', 'size'
                    ).get(product_id=product_id, color_id=color_id, size__name=size_name,
                          product__is_active=True, color__is_active=True, size__is_active=True)
                except ProductSizeStock.DoesNotExist:
                    raise serializers.ValidationError({'items': 'Товар или размер недоступен.'})
                if stock.available < quantity:
                    raise serializers.ValidationError({'items': f'Недостаточно товара: {stock.product.name}, {size_name}.'})
                rows.append((stock, quantity))
            order = Order.objects.create(order_number=f'KISA-{uuid.uuid4().hex[:12].upper()}', **validated_data)
            subtotal = Decimal('0')
            for stock, quantity in rows:
                product = stock.product
                OrderItem.objects.create(
                    order=order, product=product, color=stock.color, size=stock.size,
                    product_name=product.name, product_sku=product.slug,
                    color_name=stock.color.name, size_name=stock.size.name, quantity=quantity,
                    price_rub=product.price_rub, price_kgs=product.price_kgs,
                    total_rub=product.price_rub * quantity, total_kgs=product.price_kgs * quantity,
                )
                subtotal += (product.price_kgs if order.currency == 'KGS' else product.price_rub) * quantity
                stock.reserved += quantity
                stock.save(update_fields=['reserved', 'updated_at'])
            order.subtotal = order.total = subtotal
            order.save(update_fields=['subtotal', 'total', 'updated_at'])
            return order

    def to_representation(self, instance):
        return OrderDetailSerializer(instance, context=self.context).data
