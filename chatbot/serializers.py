from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'icon', 'badge', 'badge_type',
            'price', 'price_display', 'description', 'specs',
            'highlights', 'in_stock'
        ]

    def get_price_display(self, obj):
        return obj.price_display()