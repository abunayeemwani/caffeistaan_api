from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # 01. Kitchen Display (KDS)
    path('kds/', views.KitchenDisplayView.as_view(), name='kds'),
    path('kds/feed/', views.KDSOrderFeedView.as_view(), name='kds_feed'),
    path('orders/<str:order_number>/update-status/', views.UpdateOrderStatusView.as_view(), name='update_status'),
    path('orders/<str:order_number>/kot/', views.PrintKOTView.as_view(), name='print_kot'),

    # 02. Menu & Stock Manager
    path('menu/', views.MenuStockManagerView.as_view(), name='menu_manager'),
    path('menu/<int:pk>/toggle-availability/', views.ToggleDishStockView.as_view(), name='toggle_dish_stock'),

    # 03. Reservation & Sales Desk
    path('reservations-desk/', views.ReservationSalesDeskView.as_view(), name='reservation_desk'),
]