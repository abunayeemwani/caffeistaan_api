from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.MobileCheckoutAPIView.as_view(), name='mobile_checkout'),
    path('my-orders/', views.CustomerOrderHistoryAPIView.as_view(), name='customer_order_history'),  # <--- Add this line
    path('<str:order_number>/track/', views.OrderTrackAPIView.as_view(), name='track_order'),
]