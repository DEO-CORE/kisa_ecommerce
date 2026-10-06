from rest_framework import serializers
from journal.models import Publication, PublicationProduct
from catalog.api.serializers import ProductListSerializer


class PublicationProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=PublicationProduct._meta.get_field('product').related_model.objects.all(),
        source='product',
        write_only=True
    )
    
    class Meta:
        model = PublicationProduct
        fields = ('id', 'product', 'product_id', 'order', 'note')


class PublicationListSerializer(serializers.ModelSerializer):
    preview_image_url = serializers.SerializerMethodField()
    type_badge_class = serializers.CharField(source='get_type_badge_class', read_only=True)
    
    class Meta:
        model = Publication
        fields = ('id', 'title', 'slug', 'pub_type', 'type_badge_class', 'published_at', 
                  'preview_image', 'preview_image_url', 'preview_text', 'is_featured', 'order')
    
    def get_preview_image_url(self, obj):
        if obj.preview_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview_image.url)
            return obj.preview_image.url
        return None


class PublicationDetailSerializer(serializers.ModelSerializer):
    preview_image_url = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()
    products = PublicationProductSerializer(source='publication_products', many=True, read_only=True)
    type_badge_class = serializers.CharField(source='get_type_badge_class', read_only=True)
    
    class Meta:
        model = Publication
        fields = ('id', 'title', 'slug', 'pub_type', 'type_badge_class', 'published_at',
                  'preview_image', 'preview_image_url', 'hero_image', 'hero_image_url',
                  'preview_text', 'content', 'products', 'is_published', 'is_featured', 'order',
                  'meta_title', 'meta_description', 'meta_keywords', 'created_at', 'updated_at')
    
    def get_preview_image_url(self, obj):
        if obj.preview_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview_image.url)
            return obj.preview_image.url
        return None
    
    def get_hero_image_url(self, obj):
        if obj.hero_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None