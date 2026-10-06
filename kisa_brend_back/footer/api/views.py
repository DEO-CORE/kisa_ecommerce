from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from footer.models import Contacts, Partnership, Support, InfoPage, SiteSettings
from .serializers import ContactsSerializer, PartnershipSerializer, SupportSerializer, InfoPageSerializer, SiteSettingsSerializer


class SiteSettingsView(APIView):
    def get(self, request):
        settings = SiteSettings.get_solo()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)


class ContactsView(APIView):
    def get(self, request):
        contacts = Contacts.get_solo()
        serializer = ContactsSerializer(contacts)
        return Response(serializer.data)


class PartnershipView(APIView):
    def get(self, request):
        partnership = Partnership.get_solo()
        serializer = PartnershipSerializer(partnership)
        return Response(serializer.data)


class SupportView(APIView):
    def get(self, request):
        support = Support.get_solo()
        serializer = SupportSerializer(support)
        return Response(serializer.data)


class InfoPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InfoPage.objects.filter(is_active=True).order_by('page_type')
    serializer_class = InfoPageSerializer
    lookup_field = 'page_type'
    filter_backends = []