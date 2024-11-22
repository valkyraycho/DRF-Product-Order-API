from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Order, User


class UserOrderTestCase(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create(username="user1", password="test")
        user2 = User.objects.create(username="user2", password="test")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self) -> None:
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        response = self.client.get(reverse("user-order-list"))
        assert response.status_code == status.HTTP_200_OK
        assert all(order["user"] == user.username for order in response.json())

    def test_user_order_unauthenticated(self) -> None:
        response = self.client.get(reverse("user-order-list"))
        assert response.status_code == status.HTTP_403_FORBIDDEN
