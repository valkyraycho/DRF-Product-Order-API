from collections.abc import Sequence

from django.db.models import Max, QuerySet
from rest_framework import filters, generics
from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .filtersets import ProductFilterSet
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer, ProductsInfoSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilterSet
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "description")
    ordering_fields = ("name", "price", "stock")

    def get_permissions(self) -> Sequence[BasePermission]:
        self.permission_classes = (IsAuthenticated,)
        if self.request.method == "POST":
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()  # type: ignore


class ProductDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self) -> Sequence[BasePermission]:
        self.permission_classes = (IsAuthenticated,)
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()  # type: ignore


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


class OrderDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.prefetch_related("user", "items__product")
    serializer_class = OrderSerializer
