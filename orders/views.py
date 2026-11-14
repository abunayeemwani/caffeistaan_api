from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404

from menu.models import Dish, DishVariant, AddOn
from .models import Order, OrderItem, OrderStatusHistory
from .services import OrderService
from .serializers import CheckoutRequestSerializer, OrderDetailSerializer
from .notifications import NotificationService
from core.models import CafeConfiguration


class CustomerOrderHistoryAPIView(generics.ListAPIView):
    """
    GET /api/v1/orders/my-orders/
    Returns past orders placed by the authenticated customer.
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items').order_by('-created_at')


class MobileCheckoutAPIView(APIView):
    """
    POST /api/v1/orders/checkout/
    Validates cart contents against the database, computes totals on server,
    and returns a confirmed Cash on Delivery order.
    """
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        config = CafeConfiguration.get_solo()

        # 1. Check if café is accepting orders
        if not config.is_ordering_open:
            return Response(
                {"error": config.closure_message or "Ordering is temporarily paused."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CheckoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        subtotal = Decimal('0.00')
        evaluated_items = []

        # 2. Server-side authoritative price calculation
        for line in data['items']:
            dish = Dish.objects.select_for_update().get(id=line['dish_id'], is_available=True)
            unit_price = dish.current_price
            variant_name = ""

            # Check variant price
            if line.get('variant_id'):
                variant = DishVariant.objects.get(id=line['variant_id'], dish=dish)
                unit_price += variant.price_adjustment
                variant_name = variant.name

            # Check add-ons
            addon_names = []
            if line.get('addon_ids'):
                addons = AddOn.objects.filter(id__in=line['addon_ids'], dish=dish, is_available=True)
                for addon in addons:
                    unit_price += addon.price
                    addon_names.append(f"{addon.name} (+{addon.price})")

            line_total = unit_price * line['quantity']
            subtotal += line_total

            evaluated_items.append({
                'dish': dish,
                'dish_name': dish.name,
                'variant_name': variant_name,
                'addons_summary': ", ".join(addon_names),
                'unit_price': unit_price,
                'quantity': line['quantity'],
                'line_total': line_total,
                'special_instructions': line.get('special_instructions', '')
            })

        order_type = data['order_type']

        # 3. Dynamic delivery fee based on order type & free delivery threshold
        delivery_fee = Decimal('0.00')
        if order_type == Order.OrderType.DELIVERY:
            if subtotal < config.free_delivery_threshold:
                delivery_fee = config.delivery_fee.quantize(Decimal('0.01'))

        # 4. Dynamic GST calculation from the model
        tax_rate = config.gst_percentage / Decimal('100.00')
        tax_amount = (subtotal * tax_rate).quantize(Decimal('0.01'))

        # 5. Grand total
        total_amount = subtotal + tax_amount + delivery_fee

        order = Order.objects.create(
            order_number=OrderService.generate_order_number(),
            user=request.user if request.user.is_authenticated else None,
            order_type=order_type,
            order_status=Order.OrderStatus.PENDING,
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            customer_email=data.get('customer_email', ''),
            delivery_street_address=data.get('delivery_street_address', ''),
            delivery_locality=data.get('delivery_locality', ''),
            delivery_instructions=data.get('delivery_instructions', ''),
            dine_in_table_number=data.get('dine_in_table_number', ''),
            pickup_time=data.get('pickup_time'),
            subtotal=subtotal,
            tax_amount=tax_amount,
            delivery_fee=delivery_fee,
            discount_amount=Decimal('0.00'),
            total_amount=total_amount,
            payment_method="Cash on Delivery (COD)",
            notes=data.get('notes', '')
        )

        NotificationService.notify_kitchen_new_order(order)

        for item_data in evaluated_items:
            OrderItem.objects.create(
                order=order,
                dish=item_data['dish'],
                dish_name=item_data['dish_name'],
                variant_name=item_data['variant_name'],
                addons_summary=item_data['addons_summary'],
                unit_price=item_data['unit_price'],
                quantity=item_data['quantity'],
                line_total=item_data['line_total'],
                special_instructions=item_data['special_instructions']
            )

        OrderStatusHistory.objects.create(
            order=order,
            status=Order.OrderStatus.PENDING,
            comments="Order successfully placed via Mobile App (Cash on Delivery)."
        )

        return Response({
            "success": True,
            "order_number": order.order_number,
            "total_amount": str(order.total_amount),
            "payment_method": "Cash on Delivery (COD)"
        }, status=status.HTTP_201_CREATED)


class OrderTrackAPIView(APIView):
    """
    GET /api/v1/orders/<order_number>/track/
    Returns live fulfillment stepper and details.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, order_number):
        order = get_object_or_404(Order.objects.prefetch_related('items', 'status_history'), order_number=order_number)
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)