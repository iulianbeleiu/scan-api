from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product


CART_URL = reverse('shop:cart')


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
        product = Product.objects.create(
            user=self.user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='3532452342',
        )

        payload = {
            'product': [product.id],
            'quantity': product.quantity,
        }
        res_put = self.client.put(CART_URL, payload)
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)

        res = self.client.get(CART_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['products'][0], product.id)
