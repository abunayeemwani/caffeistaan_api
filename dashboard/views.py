from decimal import Decimal
from django.views.generic import TemplateView, View, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from orders.models import Order
from orders.services import OrderService
from menu.models import Dish, MenuCategory


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or getattr(user, 'is_cafe_staff', False))


# ----------------------------------------------------
# 01. KITCHEN DISPLAY (KDS) - 4-COLUMN KANBAN
# ----------------------------------------------------
class KitchenDisplayView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/kds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_orders = Order.objects.exclude(
            order_status__in=[Order.OrderStatus.COMPLETED, Order.OrderStatus.CANCELLED, Order.OrderStatus.REJECTED]
        ).prefetch_related('items').order_by('created_at')

        context['pending_orders'] = active_orders.filter(order_status=Order.OrderStatus.PENDING)
        context['accepted_orders'] = active_orders.filter(order_status=Order.OrderStatus.ACCEPTED)
        context['preparing_orders'] = active_orders.filter(order_status=Order.OrderStatus.PREPARING)
        context['ready_orders'] = active_orders.filter(order_status=Order.OrderStatus.READY)
        return context


class KDSOrderFeedView(StaffRequiredMixin, View):
    """Polled by HTMX every 8s; returns the 4 Kanban columns."""
    def get(self, request, *args, **kwargs):
        active_orders = Order.objects.exclude(
            order_status__in=[Order.OrderStatus.COMPLETED, Order.OrderStatus.CANCELLED, Order.OrderStatus.REJECTED]
        ).prefetch_related('items').order_by('created_at')

        return render(request, 'dashboard/partials/kds_kanban_columns.html', {
            'pending_orders': active_orders.filter(order_status=Order.OrderStatus.PENDING),
            'accepted_orders': active_orders.filter(order_status=Order.OrderStatus.ACCEPTED),
            'preparing_orders': active_orders.filter(order_status=Order.OrderStatus.PREPARING),
            'ready_orders': active_orders.filter(order_status=Order.OrderStatus.READY),
        })


class UpdateOrderStatusView(StaffRequiredMixin, View):
    def post(self, request, order_number, *args, **kwargs):
        order = get_object_or_404(Order, order_number=order_number)
        new_status = request.POST.get('new_status')

        try:
            OrderService.advance_order_status(
                order=order,
                new_status=new_status,
                staff_user=request.user,
                notes=request.POST.get('comments', '')
            )
        except ValueError as err:
            return HttpResponseBadRequest(str(err))

        active_orders = Order.objects.exclude(
            order_status__in=[Order.OrderStatus.COMPLETED, Order.OrderStatus.CANCELLED, Order.OrderStatus.REJECTED]
        ).prefetch_related('items').order_by('created_at')

        return render(request, 'dashboard/partials/kds_kanban_columns.html', {
            'pending_orders': active_orders.filter(order_status=Order.OrderStatus.PENDING),
            'accepted_orders': active_orders.filter(order_status=Order.OrderStatus.ACCEPTED),
            'preparing_orders': active_orders.filter(order_status=Order.OrderStatus.PREPARING),
            'ready_orders': active_orders.filter(order_status=Order.OrderStatus.READY),
        })


class PrintKOTView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'dashboard/print_kot.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'


# ----------------------------------------------------
# 02. MENU & STOCK MANAGER
# ----------------------------------------------------
class MenuStockManagerView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/menu_manager.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        dishes = Dish.objects.select_related('category').prefetch_related('images').all()
        if search_query:
            dishes = dishes.filter(name__icontains=search_query)

        context['dishes'] = dishes
        context['search_query'] = search_query
        return context


class ToggleDishStockView(StaffRequiredMixin, View):
    """HTMX toggle for dish availability."""
    def post(self, request, pk, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=pk)
        dish.is_available = not dish.is_available
        dish.save(update_fields=['is_available', 'updated_at'])
        return render(request, 'dashboard/partials/stock_toggle_button.html', {'dish': dish})


# ----------------------------------------------------
# 03. RESERVATION & SALES DESK
# ----------------------------------------------------
class ReservationSalesDeskView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/reservation_desk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Sales metrics
        today_orders = Order.objects.filter(created_at__date=today)
        context['today_revenue'] = today_orders.filter(order_status=Order.OrderStatus.COMPLETED).aggregate(
            val=Sum('total_amount')
        )['val'] or Decimal('0.00')
        context['active_orders_count'] = today_orders.exclude(
            order_status__in=[Order.OrderStatus.COMPLETED, Order.OrderStatus.CANCELLED]
        ).count()

        # Floor plan tables (T-01 to T-12 matching Screen 03)
        context['tables'] = [
            {'num': 'T-01', 'status': 'available'},
            {'num': 'T-02', 'status': 'available'},
            {'num': 'T-03', 'status': 'seated'},
            {'num': 'T-04', 'status': 'seated'},
            {'num': 'T-05', 'status': 'available'},
            {'num': 'T-06', 'status': 'available'},
            {'num': 'T-07', 'status': 'booked'},
            {'num': 'T-08', 'status': 'seated'},
            {'num': 'T-09', 'status': 'booked'},
            {'num': 'T-10', 'status': 'seated'},
            {'num': 'T-11', 'status': 'booked'},
            {'num': 'T-12', 'status': 'booked'},
        ]

        # Upcoming bookings feed
        context['upcoming_bookings'] = [
            {'name': 'Rahul G.', 'guests': 4, 'time': '8:00 PM'},
            {'name': 'Rahul L.', 'guests': 4, 'time': '8:00 PM'},
            {'name': 'Rahul G.', 'guests': 4, 'time': '8:00 PM'},
            {'name': 'Rahul G.', 'guests': 4, 'time': '8:00 PM'},
            {'name': 'Rout G.', 'guests': 4, 'time': '9:00 PM'},
        ]
        return context