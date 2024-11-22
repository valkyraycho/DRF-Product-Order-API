from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.product_list_view, name="product-list"),
    path("products/<int:pk>/", views.product_detail_view, name="product-detail"),
    path("products/info/", views.products_info_view, name="products-info"),
    path("orders/", views.order_list_view, name="order-list"),
    path("orders/<int:pk>/", views.order_detail_view, name="order-detail"),
]
