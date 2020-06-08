from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product
from shop.serializer import ProductSerializer


PRODUCT_URL = reverse('shop:product-list')


def detail_url(product_id):
    """Return Product detail URL"""
    return reverse('shop:product-detail', args=[product_id])


def shop_product_barcode_url(barcode):
    return reverse('shop:product-barcode', args=[barcode])


class PrivateProductTests(TestCase):
    """Test that Product API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required when accessing the Shop API"""
        res = self.client.get(PRODUCT_URL)

        self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicProductTests(TestCase):
    """Test that authenticated user can access the Product API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test123'
        )
        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving shops"""
        Product.objects.create(
            user=self.user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='1239832798432',
        )
        Product.objects.create(
            user=self.user,
            name='Product name 2',
            description='Product description 2',
            quantity=100,
            price=5,
            barcode='1239832798432',
        )

        res = self.client.get(PRODUCT_URL)
        serializer = ProductSerializer(res.data, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_limited_to_user(self):
        """Test that returned products are for authenticated user only"""
        product = Product.objects.create(
            user=self.user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='1239832798432',
        )
        Product.objects.create(
            user=get_user_model().objects.create_user(
                email='test2@test.com',
                password='test123'
            ),
            name='Product name x',
            description='Product description x',
            quantity=24,
            price=123,
            barcode='231543153432',
        )

        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], product.name)

    def test_create_product_successful(self):
        """Test creating a product is successful"""
        payload = {
            'name': 'Product name 1',
            'description': 'Product description 1',
            'quantity': 5,
            'price': 10,
            'barcode': '1239832798432',
        }
        self.client.post(PRODUCT_URL, payload)

        exists = Product.objects.filter(
            user=self.user, name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_product_invalid(self):
        """Test creating a product with invalid payload"""
        payload = {
            'name': '',
            'description': '',
            'quantity': 5,
            'price': 10,
            'barcode': '',
        }
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_product_detail(self):
        """Test viewing product detail"""
        product = Product.objects.create(
            user=self.user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='1239832798432',
        )

        res = self.client.get(detail_url(product.id))
        serializer = ProductSerializer(product)

        self.assertEqual(res.data, serializer.data)

    def test_get_shop_product_by_barcode(self):
        """Test get a shop product by barcode"""
        product1 = Product.objects.create(
            user=self.user,
            name='Product name 1',
            description='Product description 1',
            quantity=5,
            price=10,
            barcode='1239832798432',
        )

        Product.objects.create(
            user=self.user,
            name='Product name 2',
            description='Product description 2',
            quantity=100,
            price=5,
            barcode='54352345234',
        )

        res = self.client.get(shop_product_barcode_url(product1.barcode))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ProductSerializer(res.data)
        self.assertEqual(product1.name, serializer.data['name'])
