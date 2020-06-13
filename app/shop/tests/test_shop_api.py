from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Shop, Product
from shop.serializers import ShopSerializer


SHOP_URL = reverse('shop:shop-list')


def detail_url(shop_id):
    """Return Shop detail URL"""
    return reverse('shop:shop-detail', args=[shop_id])


class ShopTests(TestCase):
    """Test Shop API"""

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

    def test_view_shop_detail(self):
        """Test viewing shop detail"""
        shop = Shop.objects.create(user=self.user, name='ABC Corner')

        res = self.client.get(detail_url(shop.id))
        serializer = ShopSerializer(shop)

        self.assertEqual(res.data, serializer.data)

    def test_create_shop_with_products(self):
        """Test creating a shop with products"""
        product1 = Product.objects.create(
            user=self.user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='98769868768',
        )

        product2 = Product.objects.create(
            user=self.user,
            name='Product name 2',
            description='Product description 2',
            quantity=100,
            price=5,
            barcode='1239832798432',
        )

        payload = {
            'name': 'ABC Corner',
            'products': [product1.id, product2.id]
        }

        res = self.client.post(SHOP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        shop = Shop.objects.get(id=res.data['id'])
        products = shop.products.all()

        self.assertEqual(len(products), 2)
        self.assertIn(product1, products)
        self.assertIn(product2, products)
