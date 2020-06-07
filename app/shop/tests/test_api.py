from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Shop
from shop.serializer import ShopSerializer


SHOP_URL = reverse('shop:shop-list')


class PrivateShopTests(TestCase):
    """Test that Shop API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required when accessing the Shop API"""
        res = self.client.get(SHOP_URL)

        self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicShopTests(TestCase):
    """Test that authenticated user can access the Shop API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test123'
        )
        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def test_retrieve_shops(self):
        """Test retrieving shops"""
        Shop.objects.create(user=self.user, name='ABC Iulian')
        Shop.objects.create(user=self.user, name='Market X')

        res = self.client.get(SHOP_URL)
        serializer = ShopSerializer(res.data, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_shops_limited_to_user(self):
        """Test that returned shops are for authenticated user only"""
        shop = Shop.objects.create(user=self.user, name='ABC Corner')
        Shop.objects.create(user=get_user_model().objects.create_user(
            email='test2@test.com',
            password='test123'
        ), name='Non-stop')

        res = self.client.get(SHOP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], shop.name)

    def test_create_shop_successful(self):
        """Test creating a Shop is successful"""
        payload = {'name': 'ABC Corner'}
        self.client.post(SHOP_URL, payload)

        exists = Shop.objects.filter(
            user=self.user, name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_shop_invalid(self):
        """Test creating a shop with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(SHOP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
