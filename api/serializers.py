from decimal import Decimal

from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer[Product]):
    price = serializers.FloatField()

    class Meta:
        model = Product
        fields = ("name", "description", "price", "stock")

    def validate_price(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class ProductsInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, read_only=True)
    count = serializers.IntegerField(read_only=True)
    max_price = serializers.FloatField(read_only=True)


class OrderItemSerializer(serializers.ModelSerializer[OrderItem]):
    product = serializers.StringRelatedField()
    price = serializers.FloatField(source="product.price")

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "price", "item_subtotal")


class OrderSerializer(serializers.ModelSerializer[Order]):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("order_id", "user", "created_at", "status", "items", "total_price")

    def get_total_price(self, obj: Order) -> Decimal:
        return sum(item.item_subtotal for item in obj.items.all())  # type: ignore
