from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from cart.models import Cart
from cart.serializers import CartSerializer

from shop.models import Shop, Address


CART_URL = reverse('cart:cart-list')
CART_ITEMS_URL = reverse('cart:cartitem-list')


def receipt_pdf_url(cart_id):
    """Return url for receipt pdf"""
    return reverse('cart:cart-receipt', args=[cart_id])


def sample_address():
    return Address.objects.create(
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


class PrivateCartTests(TestCase):
    """Test that Cart API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_retrieving_cart(self):
        """Test that login is required"""
        res = self.client.get(CART_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_receipt_pdf(self):
        """Test that login is required when generating receipt"""
        res = self.client.get(receipt_pdf_url(0))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicCartTests(TestCase):
    """Test the authorized Cart API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test567'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.shop = Shop.objects.create(
            user=self.user,
            name='ABC Iulian',
            address=sample_address(),
        )

    def test_retrieve_cart(self):
        """Test retrieving cart"""
        cart_item_payload = {
            'name': "Sample cart item test",
            'price': 5,
            'quantity': 5,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)

        cart = Cart.objects.create(
            user=self.user,
            total=25,
            shop=self.shop,
        )

        cart.items.add(res_items.data['id'])
        cart.refresh_from_db()
        res_cart = self.client.get(CART_URL)
        cart_object = Cart.objects.all()
        cart_serializer = CartSerializer(cart_object, many=True)

        self.assertEqual(res_cart.status_code, status.HTTP_200_OK)
        self.assertEqual(res_cart.data, cart_serializer.data)

    def test_cart_limited_to_user(self):
        """Test that returned cart is for authenticated user"""
        cart = Cart.objects.create(
            user=self.user,
            total=25,
            shop=self.shop,
        )
        cart_item_payload = {
            'name': "Sample cart item test",
            'price': 5,
            'quantity': 5,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)
        cart.items.add(res_items.data['id'])

        other_user = get_user_model().objects.create(
            email="popescu@test.com",
            password='popescu431',
        )
        Cart.objects.create(
            user=other_user,
            total=15,
            shop=self.shop,
        )
        cart.items.add(res_items.data['id'])

        res_cart = self.client.get(CART_URL)
        self.assertEqual(res_cart.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_cart.data), 1)
        self.assertEqual(res_cart.data[0]['total'], cart.total)

    def test_create_cart_successful(self):
        """Test creating a cart"""
        cart_item_payload = {
            'name': "Sample cart item test",
            'price': 2,
            'quantity': 7,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)
        payload = {
            'total': 14,
            'shop': self.shop.id,
            'items': [res_items.data['id']],
        }

        self.client.post(CART_URL, payload)
        exists = Cart.objects.filter(
            user=self.user,
            total=payload['total']
        ).exists()

        self.assertTrue(exists)

    def test_create_cart_invalid(self):
        """Test creating a cart with invalid payload"""
        payload = {
            'total': '',
            'items': []
        }

        res = self.client.post(CART_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_receipt_file_download(self):
        """Test that pdf is attached to response"""
        cart_item_payload = {
            'name': "Sample cart item pdf",
            'price': 5,
            'quantity': 2,
        }

        res_items = self.client.post(CART_ITEMS_URL, cart_item_payload)
        payload = {
            'total': 14,
            'shop': self.shop.id,
            'items': [res_items.data['id']]
        }
        res = self.client.post(CART_URL, payload)

        pdf_url = receipt_pdf_url(res.data['id'])
        pdf_file_name = f'receipt-{str(res.data["id"])}.pdf'
        pdf_res = self.client.get(pdf_url)

        self.assertEqual(pdf_res.status_code, status.HTTP_200_OK)
        self.assertEqual(pdf_res.get('Content-Disposition'),
                         f'attachment; filename="{pdf_file_name}"')

    def test_receipt_file_invalid(self):
        """Test that pdf is not generated when cart is not found"""

        pdf_url = receipt_pdf_url(0)
        res = self.client.get(pdf_url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
