from rest_framework import serializers
from .models import MenuCategory, Dish, DishVariant, AddOn, DishImage


class DishImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishImage
        fields = ['id', 'image', 'alt_text', 'is_primary']


class DishVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishVariant
        fields = ['id', 'name', 'price_adjustment', 'is_default']


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = ['id', 'name', 'price', 'is_available']


class DishSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    variants = DishVariantSerializer(many=True, read_only=True)
    addons = AddOnSerializer(many=True, read_only=True)
    images = DishImageSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'detailed_description',
            'base_price',
            'discounted_price',
            'current_price',
            'preparation_time',
            'dietary_type',
            'is_available',
            'is_featured',
            'variants',
            'addons',
            'images',
        ]


class MenuCategorySerializer(serializers.ModelSerializer):
    """Returns categories with their active dishes nested inside."""
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'slug', 'description', 'display_order', 'dishes']

    def get_dishes(self, obj):
        active_dishes = obj.dishes.filter(is_available=True)
        return DishSerializer(active_dishes, many=True, context=self.context).data
