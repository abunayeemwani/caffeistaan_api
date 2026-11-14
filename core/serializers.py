from rest_framework import serializers
from .models import CafeConfiguration

class CafeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeConfiguration
        fields = [
            'cafe_name',
            'cafe_tagline',
            'cafe_description',
            'cafe_phone',
            'cafe_email',
            'cafe_address',
            'currency_symbol',
            'gst_percentage',
            'delivery_fee',
            'free_delivery_threshold',
            'is_ordering_open',
            'closure_message',
        ]