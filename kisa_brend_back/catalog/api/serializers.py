from rest_framework import serializers
from catalog.models import Drop, Color, Size, Product, ProductColor, ProductImage, ProductSizeStock


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'slug', 'hex_code', 'is_active', 'order')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name', 'order', 'is_active')


class DropSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Drop
        fields = ('id', 'name', 'slug', 'is_active', 'order', 'description', 'image', 'products_count', 'created_at')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt', 'order')


class ProductColorSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), source='color', write_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductColor
        fields = ('id', 'color', 'color_id', 'is_main', 'order', 'images')


class ProductSizeStockSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), source='size', write_only=True)
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), source='color', write_only=True)
    available = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ProductSizeStock
        fields = ('id', 'size', 'size_id', 'color', 'color_id', 'quantity', 'reserved', 'available', 'is_low_stock', 'is_out_of_stock')


class ProductListSerializer(serializers.ModelSerializer):
    drop = DropSerializer(read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()
    total_stock = serializers.IntegerField(source='get_total_stock', read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'drop', 'price_rub', 'price_kgs', 'main_image_url', 'colors', 'is_active', 'is_new', 'is_bestseller', 'total_stock', 'order')
    
    def get_main_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
            return obj.main_image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    drop = DropSerializer(read_only=True)
    drop_id = serializers.PrimaryKeyRelatedField(queryset=Drop.objects.all(), source='drop', write_only=True, allow_null=True, required=False)
    colors = ProductColorSerializer(source="product_colors", many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stocks = ProductSizeStockSerializer(many=True, read_only=True)
    available_sizes = serializers.SerializerMethodField()
    total_stock = serializers.IntegerField(source='get_total_stock', read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'drop', 'drop_id', 'price_rub', 'price_kgs', 'description', 'composition', 'fit_recommendation', 
                  'main_image', 'colors', 'images', 'stocks', 'available_sizes', 'total_stock',
                  'is_active', 'is_new', 'is_bestseller', 'order', 'meta_title', 'meta_description', 'meta_keywords',
                  'created_at', 'updated_at')
    
    def get_available_sizes(self, obj):
        stocks = obj.stocks.filter(quantity__gt=0).select_related('size', 'color')
        return ProductSizeStockSerializer(stocks, many=True, context=self.context).data


class ProductColorDetailSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), source='color', write_only=True)
    
    class Meta:
        model = ProductColor
        fields = ('id', 'color', 'color_id', 'is_main', 'order')


class ProductImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt', 'order')