from django.db.models import Max
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer, ProductsInfoSerializer

# @api_view(["GET"])
# def product_list_view(request: Request) -> Response:
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


# @api_view(["GET"])
# def product_detail_view(request: Request, pk: int) -> Response:
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
def products_info_view(request: Request) -> Response:
    products = Product.objects.all()
    serializer = ProductsInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data)


# @api_view(["GET"])
# def order_list_view(request: Request) -> Response:
#     orders = Order.objects.prefetch_related("items__product")
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer


# @api_view(["GET"])
# def order_detail_view(request: Request, pk: int) -> Response:
#     order = get_object_or_404(Order, pk=pk)
#     serializer = OrderSerializer(order)
#     return Response(serializer.data)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
