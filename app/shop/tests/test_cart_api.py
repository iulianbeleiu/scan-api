from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product


CART_URL = reverse('shop:cart')


def sample_product(user):
    return Product.objects.create(
            user=user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='3532452342',
        )


class PrivateCartTests(TestCase):
    """Test that login Cart API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required when using Cart API"""
        res = self.client.get(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicCartTests(TestCase):
    """Test that authenticated user can access the Cart API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='iulian@iulian.com',
            password='test123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_cart(self):
        """Test retrieving cart"""
        product = sample_product(self.user)

        payload = {
            'products': [product.id],
            'quantity': 2,
        }
        res_put = self.client.put(CART_URL, payload)
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)

        res = self.client.get(CART_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['products'][0], product.id)
        self.assertEqual(res.data['total'],
                         payload['quantity'] * product.price)

    def test_add_to_cart_high_quantity(self):
        """Test cannot add product to cart with higher quantity"""
        product = sample_product(self.user)
        payload = {
            'products': [product.id],
            'quantity': 9999999999
        }

        res = self.client.put(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
