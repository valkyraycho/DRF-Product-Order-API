from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"
    ),
    path("products/info/", views.products_info_view, name="products-info"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/user/", views.UserOrderListView.as_view(), name="user-order-list"),
    path("orders/<uuid:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
]
