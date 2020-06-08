from django.test import TestCase
from django.contrib.auth import get_user_model

from shop.models import Shop, Product


def sample_user():
    email = 'test@test.com'
    password = 'test123'

    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_shop(self):
        """Test the shop string representation"""
        shop = Shop.objects.create(
            user=sample_user(),
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
