from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import CafeConfiguration
from .serializers import CafeConfigSerializer

class CafeConfigAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        config = CafeConfiguration.get_solo()
        serializer = CafeConfigSerializer(config)
        return Response(serializer.data)