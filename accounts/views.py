from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/
    Registers a new customer account using phone, full_name, and password.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "success": True,
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "full_name": user.full_name,
                "is_staff": user.is_staff or getattr(user, 'is_cafe_staff', False),
            }
        }, status=status.HTTP_201_CREATED)


class MeAPIView(APIView):
    """
    GET /api/v1/auth/me/
    Returns the profile and role data of the currently authenticated JWT user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)