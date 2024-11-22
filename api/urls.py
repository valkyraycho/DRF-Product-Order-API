from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.ProductListCreateView.as_view(), name="product-list"),
    path(
        "products/<int:pk>/",
        views.ProductDetailUpdateDestroyView.as_view(),
        name="product-detail",
    ),
    path("products/info/", views.ProductInfoView.as_view(), name="products-info"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/user/", views.UserOrderListView.as_view(), name="user-order-list"),
    path(
        "orders/<uuid:pk>/",
        views.OrderDetailUpdateDestroyView.as_view(),
        name="order-detail",
    ),
]
