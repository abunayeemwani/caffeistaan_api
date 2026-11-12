from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MenuCategory, Dish
from .serializers import MenuCategorySerializer, DishSerializer


class MenuCatalogAPIView(generics.ListAPIView):
    """
    GET /api/v1/menu/
    Returns all active categories nested with their available dishes.
    """
    queryset = MenuCategory.objects.filter(is_active=True).prefetch_related(
        'dishes__variants',
        'dishes__addons',
        'dishes__images'
    )
    serializer_class = MenuCategorySerializer
    permission_classes = [permissions.AllowAny]


class DishDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/v1/menu/dishes/<slug>/
    Returns complete detail for a single dish.
    """
    queryset = Dish.objects.filter(is_available=True).prefetch_related('variants', 'addons', 'images')
    serializer_class = DishSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class ToggleDishAvailabilityAPIView(APIView):
    """
    PATCH /api/v1/menu/dishes/<id>/toggle/
    Allows café staff to instantly toggle a dish In-Stock or Sold-Out.
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        dish = get_object_or_404(Dish, pk=pk)
        dish.is_available = not dish.is_available
        dish.save(update_fields=['is_available', 'updated_at'])
        return Response({
            "id": dish.id,
            "name": dish.name,
            "is_available": dish.is_available
        }, status=status.HTTP_200_OK)
