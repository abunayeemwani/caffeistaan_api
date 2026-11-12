from firebase_admin import messaging
from accounts.models import FCMDevice

class NotificationService:
    @staticmethod
    def notify_kitchen_new_order(order):
        """Sends a high-priority data message that triggers an audio chime on staff devices."""
        staff_tokens = list(
            FCMDevice.objects.filter(is_staff_device=True).values_list('registration_id', flat=True)
        )
        if not staff_tokens:
            return

        message = messaging.MulticastMessage(
            data={
                'type': 'NEW_ORDER',
                'order_number': order.order_number,
                'total_amount': str(order.total_amount),
                'order_type': order.order_type,
                'customer_name': order.customer_name,
                'play_sound': 'true',
            },
            tokens=staff_tokens,
            android=messaging.AndroidConfig(priority='high'),
        )
        try:
            messaging.send_multicast(message)
        except Exception as e:
            print(f"FCM Kitchen notification error: {e}")

    @staticmethod
    def notify_customer_status_change(order):
        """Sends standard push alert to the customer when their order progresses."""
        if not order.user:
            return

        tokens = list(
            FCMDevice.objects.filter(user=order.user).values_list('registration_id', flat=True)
        )
        if not tokens:
            return

        status_messages = {
            'ACCEPTED': 'Your Caffiestaan order has been accepted!',
            'PREPARING': 'Your brew & dishes are currently being prepared.',
            'READY': 'Your order is packed and ready!',
            'DISPATCHED': 'Your rider is on the way with your warm order.',
            'COMPLETED': 'Delivered! Enjoy your Caffiestaan experience.',
        }

        body = status_messages.get(order.order_status, f"Order status updated: {order.order_status}")

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=f"Order #{order.order_number[-6:]}",
                body=body,
            ),
            data={
                'order_number': order.order_number,
                'status': order.order_status,
            },
            tokens=tokens,
        )
        try:
            messaging.send_multicast(message)
        except Exception as e:
            print(f"FCM Customer notification error: {e}")