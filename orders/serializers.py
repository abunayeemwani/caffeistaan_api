from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory


class CartLineInputSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    addon_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
    quantity = serializers.IntegerField(min_value=1)
    special_instructions = serializers.CharField(max_length=255, required=False, allow_blank=True)


class CheckoutRequestSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=150)
    customer_phone = serializers.CharField(max_length=17)
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    order_type = serializers.ChoiceField(choices=Order.OrderType.choices)

    # Delivery specifics
    delivery_street_address = serializers.CharField(required=False, allow_blank=True)
    delivery_locality = serializers.CharField(required=False, allow_blank=True)
    delivery_instructions = serializers.CharField(required=False, allow_blank=True)

    # Dine-in / Takeaway specifics
    dine_in_table_number = serializers.CharField(required=False, allow_blank=True)
    pickup_time = serializers.DateTimeField(required=False, allow_null=True)

    notes = serializers.CharField(required=False, allow_blank=True)
    items = CartLineInputSerializer(many=True)

    def validate(self, attrs):
        order_type = attrs.get('order_type')
        if order_type == Order.OrderType.DELIVERY and not attrs.get('delivery_street_address'):
            raise serializers.ValidationError({"delivery_street_address": "Delivery street address is required for delivery orders."})
        if order_type == Order.OrderType.DINE_IN and not attrs.get('dine_in_table_number'):
            raise serializers.ValidationError({"dine_in_table_number": "Table number is required for dine-in orders."})
        if not attrs.get('items'):
            raise serializers.ValidationError({"items": "Cart cannot be empty."})
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dish_name', 'variant_name', 'addons_summary', 'unit_price', 'quantity', 'line_total', 'special_instructions']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['status', 'comments', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_number',
            'order_type',
            'order_status',
            'customer_name',
            'customer_phone',
            'delivery_street_address',
            'delivery_locality',
            'dine_in_table_number',
            'subtotal',
            'tax_amount',
            'delivery_fee',
            'discount_amount',
            'total_amount',
            'payment_method',
            'created_at',
            'items',
            'status_history',
        ]