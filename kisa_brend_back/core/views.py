from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Subscriber


class SubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Subscriber.objects.get_or_create(email=serializer.validated_data['email'].lower())
        return Response({'message': 'Вы подписаны на новости KISA.'}, status=status.HTTP_201_CREATED)
