from django.test import TestCase
from django.contrib.auth import get_user_model

from cart.models import CartItem, Cart


class ModelTests(TestCase):
    def setUp(self):
        email = 'test1@test.com'
        password = 'test123'
        self.user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

    def test_create_cart_item(self):
        """Test the cart item string representation"""
        cart_item = CartItem.objects.create(
            user=self.user,
            name="Bread",
            price=12,
            quantity=3,
        )

        self.assertEqual(str(cart_item), cart_item.name)

    def test_cart_item_total(self):
        """Test that cart item total is correct"""
        cart_item = CartItem.objects.create(
            user=self.user,
            name="Beer",
            price=5,
            quantity=6,
        )

        self.assertEqual(cart_item.total, 30)

    def test_create_cart(self):
        """Test creating a cart we get total of cart items"""
        cart_item1 = CartItem.objects.create(
            user=self.user,
            name="Beer",
            price=5,
            quantity=6,
        )
        cart_item2 = CartItem.objects.create(
            user=self.user,
            name="Bread",
            price=2,
            quantity=1,
        )

        items_total = cart_item1.total + cart_item2.total

        cart = Cart.objects.create(
            user=self.user,
            total=items_total
        )
        cart.items.add(cart_item1)
        cart.items.add(cart_item2)

        self.assertEqual(cart.total, items_total)
