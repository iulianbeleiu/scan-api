from django.test import TestCase
from django.contrib.auth import get_user_model

from shop.models import Shop


def sample_user():
    email = 'test@test.com'
    password = 'test123'

    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_shop(self):
        """Test creating a shop"""
        shop = Shop.objects.create(
            user=sample_user(),
            name='ABC Iulian',
            is_active=True,
        )

        self.assertEqual(str(shop), shop.name)
