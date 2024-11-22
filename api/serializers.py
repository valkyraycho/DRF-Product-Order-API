from decimal import Decimal

from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer[Product]):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "stock")

    def validate_price(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer[OrderItem]):
    class Meta:
        model = OrderItem
        fields = ("product", "quantity")


class OrderSerializer(serializers.ModelSerializer[Order]):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("order_id", "user", "created_at", "status", "items")
