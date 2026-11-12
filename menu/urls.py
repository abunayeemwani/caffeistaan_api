from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.MenuCatalogAPIView.as_view(), name='catalog'),
    path('dishes/<slug:slug>/', views.DishDetailAPIView.as_view(), name='dish_detail'),
    path('dishes/<int:pk>/toggle/', views.ToggleDishAvailabilityAPIView.as_view(), name='dish_toggle'),
]