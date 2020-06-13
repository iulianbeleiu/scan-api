from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from cart.models import CartItem
from cart.serializers import CartItemSerializer


CART_ITEMS_URL = reverse('cart:cartitem-list')


def sample_user():
    """Create sample user"""
    return get_user_model().objects.create(
        email='test@test.com',
        password='test123'
    )


def sample_cart_item(user):
    """Create sample cart item"""
    return CartItem.objects.create(
        user=user,
        name="Sample cart item",
        price=2,
        quantity=10,
    )


class PrivateCartItemsTests(TestCase):
    """Test that CartItems API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_retrieving_cart_items(self):
        """Test that login is required"""

        res = self.client.get(CART_ITEMS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicCartItemsTests(TestCase):
    """Test the authorized CartItems API"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='sample@test.com',
            password='sample123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_cart_items(self):
        """Test retrieving cart items"""
        sample_cart_item(self.user)

        res = self.client.get(CART_ITEMS_URL)
        serializer = CartItemSerializer(res.data, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_cart_items_limited_to_user(self):
        """Test that returned cart items are for authenticated user"""
        sample_cart_item(self.user)
        other_user = get_user_model().objects.create(
                email="xulescu@test.com",
                password='x12343x',
            )
        CartItem.objects.create(
            user=other_user,
            name="Sample cart item 2",
            price=1,
            quantity=3,
        )

        res = self.client.get(CART_ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_create_cart_items_successful(self):
        """Test creating a cart item"""
        payload = {
            'name': "Sample cart item 1",
            'price': 3,
            'quantity': 2,
        }
        self.client.post(CART_ITEMS_URL, payload)

        exists = CartItem.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_cart_items_invalid(self):
        """Test creating a cart item with invalid payload"""
        payload = {
            'name': '',
            'price': '',
            'quantity': '',
        }
        res = self.client.post(CART_ITEMS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
