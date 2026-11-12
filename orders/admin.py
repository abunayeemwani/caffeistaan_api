from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish_name', 'variant_name', 'addons_summary', 'unit_price', 'quantity', 'line_total', 'special_instructions')


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'comments', 'changed_by', 'created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_phone', 'order_type', 'order_status', 'total_amount', 'created_at')
    list_filter = ('order_status', 'order_type', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_phone')
    inlines = [OrderItemInline, OrderStatusHistoryInline]