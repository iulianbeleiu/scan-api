from django.test import TestCase

from core.tests import user_helper
from cart.models import CartItem


class ModelTests(TestCase):

    def test_create_cart_item(self):
        """Test the cart item string representation"""
        cart_item = CartItem.objects.create(
            user=user_helper.sample_user(),
            name="Bread",
            price=12,
            quantity=3,
        )

        self.assertEqual(str(cart_item), cart_item.name)

    def test_cart_item_total(self):
        """Test that cart item total is correct"""
        cart_item = CartItem.objects.create(
            user=user_helper.sample_user(),
            name="Beer",
            price=5,
            quantity=6,
        )

        self.assertEqual(cart_item.total, 30)
