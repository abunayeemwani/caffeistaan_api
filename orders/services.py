import uuid
from datetime import datetime
from django.db import transaction
from .models import Order, OrderStatusHistory
from .notifications import NotificationService


class OrderFSMService:
    VALID_TRANSITIONS = {
        Order.OrderStatus.PENDING: [
            Order.OrderStatus.ACCEPTED,
            Order.OrderStatus.REJECTED,
            Order.OrderStatus.CANCELLED
        ],
        Order.OrderStatus.ACCEPTED: [
            Order.OrderStatus.PREPARING,
            Order.OrderStatus.REJECTED,
            Order.OrderStatus.CANCELLED
        ],
        Order.OrderStatus.PREPARING: [
            Order.OrderStatus.READY,
            Order.OrderStatus.REJECTED,
            Order.OrderStatus.CANCELLED
        ],
        Order.OrderStatus.READY: [
            Order.OrderStatus.DISPATCHED,
            Order.OrderStatus.COMPLETED
        ],
        Order.OrderStatus.DISPATCHED: [
            Order.OrderStatus.COMPLETED,
            Order.OrderStatus.CANCELLED
        ],
        Order.OrderStatus.COMPLETED: [],
        Order.OrderStatus.CANCELLED: [],
        Order.OrderStatus.REJECTED: [],
    }

    @classmethod
    @transaction.atomic
    def transition_status(cls, order: Order, new_status: str, user=None, comments="") -> Order:
        if new_status not in cls.VALID_TRANSITIONS.get(order.order_status, []):
            raise ValueError(f"Cannot transition order #{order.order_number} from {order.order_status} to {new_status}.")

        order.order_status = new_status
        order.save(update_fields=['order_status', 'updated_at'])

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            comments=comments or f"Status changed to {new_status}",
            changed_by=user if (user and user.is_authenticated) else None
        )
        return order


class OrderService:
    @staticmethod
    def generate_order_number() -> str:
        """Generates a human-friendly unique ID, e.g. CAF-20261110-A9F2"""
        today_str = datetime.now().strftime('%Y%m%d')
        unique_token = uuid.uuid4().hex[:4].upper()
        return f"CAF-{today_str}-{unique_token}"

    @classmethod
    @transaction.atomic
    def advance_order_status(cls, order: Order, new_status: str, staff_user=None, notes=""):
        """Validates and advances order status with audit history."""
        valid_transitions = {
            Order.OrderStatus.PENDING: [Order.OrderStatus.ACCEPTED, Order.OrderStatus.REJECTED, Order.OrderStatus.CANCELLED],
            Order.OrderStatus.ACCEPTED: [Order.OrderStatus.PREPARING, Order.OrderStatus.CANCELLED],
            Order.OrderStatus.PREPARING: [Order.OrderStatus.READY, Order.OrderStatus.CANCELLED],
            Order.OrderStatus.READY: [Order.OrderStatus.DISPATCHED, Order.OrderStatus.COMPLETED],
            Order.OrderStatus.DISPATCHED: [Order.OrderStatus.COMPLETED, Order.OrderStatus.CANCELLED],
            Order.OrderStatus.COMPLETED: [],
            Order.OrderStatus.CANCELLED: [],
            Order.OrderStatus.REJECTED: [],
        }

        if new_status not in valid_transitions.get(order.order_status, []):
            raise ValueError(f"Cannot transition order #{order.order_number} from {order.order_status} to {new_status}")

        order.order_status = new_status
        order.save(update_fields=['order_status', 'updated_at'])

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            comments=notes or f"Order marked as {new_status}",
            changed_by=staff_user
        )

        NotificationService.notify_customer_status_change(order)

        return order