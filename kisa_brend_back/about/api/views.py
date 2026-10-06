from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from about.models import MainPageSettings, BrandPrinciple, BrandHistory, TeamBlock
from .serializers import (
    MainPageSettingsSerializer, BrandPrincipleSerializer,
    BrandHistorySerializer, TeamBlockSerializer
)


class MainPageSettingsView(APIView):
    def get(self, request):
        settings = MainPageSettings.get_solo()
        serializer = MainPageSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data)


class TeamBlockView(APIView):
    def get(self, request):
        team = TeamBlock.get_solo()
        serializer = TeamBlockSerializer(team, context={'request': request})
        return Response(serializer.data)


class BrandPrincipleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BrandPrinciple.objects.filter(is_active=True)
    serializer_class = BrandPrincipleSerializer
    filter_backends = []


class BrandHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BrandHistory.objects.filter(is_active=True)
    serializer_class = BrandHistorySerializer
    filter_backends = []