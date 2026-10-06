from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from catalog.models import Drop, Color, Size, Product, ProductColor, ProductImage, ProductSizeStock
from .serializers import (
    DropSerializer, ColorSerializer, SizeSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ProductColorSerializer, ProductImageSerializer, ProductSizeStockSerializer
)


class DropViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Drop.objects.filter(is_active=True).prefetch_related('products')
    serializer_class = DropSerializer
    lookup_field = 'slug'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.filter(is_active=True)
    serializer_class = ColorSerializer
    lookup_field = 'slug'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.filter(is_active=True)
    serializer_class = SizeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('drop').prefetch_related(
        'colors', 'images', 'stocks__size', 'stocks__color'
    )
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['drop', 'is_new', 'is_bestseller', 'colors']
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'created_at', 'price_rub']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer


class ProductColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductColor.objects.select_related('product', 'color')
    serializer_class = ProductColorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'color']


class ProductImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductImage.objects.select_related('product')
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']


class ProductSizeStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductSizeStock.objects.select_related('product', 'color', 'size')
    serializer_class = ProductSizeStockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'color', 'size']