from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from journal.models import Publication
from .serializers import PublicationListSerializer, PublicationDetailSerializer


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.filter(is_published=True).prefetch_related('products', 'publication_products__product')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['pub_type', 'is_featured']
    search_fields = ['title', 'preview_text', 'content']
    ordering_fields = ['published_at', 'order']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PublicationDetailSerializer
        return PublicationListSerializer