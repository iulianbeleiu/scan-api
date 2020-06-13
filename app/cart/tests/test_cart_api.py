from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer


CART_URL = reverse('cart:cart-list')
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


class PrivateCartTests(TestCase):
    """Test that Cart API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_retrieving_cart(self):
        """Test that login is required"""
        res = self.client.get(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicCartTests(TestCase):
    """Test the authorized Cart API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test567'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_cart(self):
        """Test retrieving cart"""
        cart_item_payload = {
            'name': "Sample cart item test",
            'price': 5,
            'quantity': 5,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)

        cart = Cart.objects.create(
            user=self.user,
            total=25
        )

        cart.items.add(res_items.data['id'])
        cart.refresh_from_db()
        res_cart = self.client.get(CART_URL)
        cart_object = Cart.objects.all()
        cart_serializer = CartSerializer(cart_object, many=True)

        self.assertEqual(res_cart.status_code, status.HTTP_200_OK)
        self.assertEqual(res_cart.data, cart_serializer.data)

    def test_cart_limited_to_user(self):
        """Test that returned cart is for authenticated user"""
        cart = Cart.objects.create(
            user=self.user,
            total=25,
        )
        cart_item_payload = {
            'name': "Sample cart item test",
            'price': 5,
            'quantity': 5,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)
        cart.items.add(res_items.data['id'])

        other_user = get_user_model().objects.create(
            email="popescu@test.com",
            password='popescu431',
        )
        Cart.objects.create(
            user=other_user,
            total=15
        )
        cart.items.add(res_items.data['id'])

        res_cart = self.client.get(CART_URL)
        self.assertEqual(res_cart.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_cart.data), 1)
        self.assertEqual(res_cart.data[0]['total'], cart.total)

    def test_create_cart_successful(self):
        """Test creating a cart"""
        cart_item_payload = {
            'name': "Sample cart item test",
            'price': 2,
            'quantity': 7,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)
        payload = {
            'total': 14,
            'items': [res_items.data['id']]
        }

        self.client.post(CART_URL, payload)
        exists = Cart.objects.filter(
            user=self.user,
            total=payload['total']
        ).exists()

        self.assertTrue(exists)

    def test_create_cart_invalid(self):
        """Test creating a cart with invalid payload"""
        payload = {
            'total': '',
            'items': []
        }

        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
