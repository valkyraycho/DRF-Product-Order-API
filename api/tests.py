from django.test import TestCase
from django.urls import reverse

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
        assert response.status_code == 200
        assert all(order["user"] == user.username for order in response.json())
