from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from shop.models import Shop, Product, product_image_file_path, Address


def sample_user():
    email = 'test@test.com'
    password = 'test123'

    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_shop(self):
        """Test the shop string representation"""
        address = Address.objects.create(
            user=get_user_model().objects.create_user(
                email='test@email.com',
                password='bestpass'
            ),
            country="Romania",
            postcode=574479,
            region="Timis",
            city="Timisoara",
            street="Gheorghe Lazar",
            number="24 A"
        )

        shop = Shop.objects.create(
            user=sample_user(),
            address=address,
            name='ABC Iulian',
            is_active=True,
        )

        self.assertEqual(str(shop), shop.name)

    def test_create_product(self):
        """Test the product string representation"""
        product = Product.objects.create(
            user=sample_user(),
            name='Product name',
            description='Product description',
            quantity=5,
            price=10,
            barcode='1239832798432',
            is_active=True
        )

        self.assertEqual(str(product), product.name)

    @patch('uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = product_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/product/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_create_address(self):
        """Test the address string representation"""
        address = Address.objects.create(
            user=sample_user(),
            country="Romania",
            postcode=574479,
            region="Timis",
            city="Timisoara",
            street="Gheorghe Lazar",
            number="24 A"
        )

        self.assertEqual(str(address), address.city)
