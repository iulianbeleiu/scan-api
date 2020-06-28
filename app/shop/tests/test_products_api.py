import tempfile
import os

from PIL import Image

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product
from shop.serializers import ProductSerializer


PRODUCT_URL = reverse('shop:product-list')


def detail_url(product_id):
    """Return Product detail URL"""
    return reverse('shop:product-detail', args=[product_id])


def shop_product_barcode_url(barcode):
    return reverse('shop:product-barcode', args=[barcode])


def image_upload_url(product_id):
    """Return url for product image upload"""
    return reverse('shop:product-upload-image', args=[product_id])


class ProductTests(TestCase):
    """Test Product API"""

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
            barcode='3532452342',
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
        serializer = ProductSerializer(res.data['results'], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

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
            name=payload['name']
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


class ProductImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            '123sfa'
        )
        self.client.force_authenticate(self.user)
        self.product = Product.objects.create(
            user=self.user,
            name='Product name x',
            description='Product description x',
            quantity=100,
            price=5,
            barcode='54352345234',
        )

    def tearDown(self):
        self.product.image.delete()

    def test_upload_image_to_product(self):
        """Test uploading an image to product"""
        url = image_upload_url(self.product.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.product.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.product.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.product.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
