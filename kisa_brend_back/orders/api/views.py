from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from orders.models import Order, OrderStatus
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user and request.user.is_staff


class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']
    queryset = Order.objects.all().prefetch_related('items')
    permission_classes = [IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'currency']
    search_fields = ['order_number', 'customer_name', 'customer_phone', 'customer_email']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']
    lookup_field = 'order_number'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('items')
        return Order.objects.none()
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, order_number=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in OrderStatus.values:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        from django.core.exceptions import ValidationError
        from orders.services import transition_order
        try:
            order = transition_order(order.pk, new_status)
        except ValidationError as exc:
            return Response({'error': exc.messages}, status=400)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)