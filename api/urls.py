from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.product_list_view),
    path("products/<int:pk>/", views.product_detail_view),
]
