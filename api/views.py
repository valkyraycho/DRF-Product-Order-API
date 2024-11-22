from collections.abc import Sequence

from django.db.models import Max, QuerySet
from rest_framework import generics
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer, ProductsInfoSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self) -> Sequence[BasePermission]:
        self.permission_classes = (IsAuthenticated,)
        if self.request.method == "POST":
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()  # type: ignore


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductInfoView(APIView):
    def get(self, request: Request) -> Response:
        products = Product.objects.all()
        serializer = ProductsInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("user", "items__product")
    serializer_class = OrderSerializer


class UserOrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("user", "items__product")
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.prefetch_related("user", "items__product")
    serializer_class = OrderSerializer
