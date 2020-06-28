from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Shop, Product, Address
from shop.serializers import ShopSerializer, AddressSerializer


SHOP_URL = reverse('shop:shop-list')


ADDRESS_URL = reverse('shop:address-list')


def detail_url(shop_id):
    """Return Shop detail URL"""
    return reverse('shop:shop-detail', args=[shop_id])


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


def address_detail_url(address_id):
    """Return Address detail URL"""
    return reverse('shop:address-detail', args=[address_id])


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
        Shop.objects.create(
            user=self.user,
            name='ABC Iulian',
            address=sample_address()
        )
        Shop.objects.create(
            user=self.user,
            name='Market X',
            address=Address.objects.create(
                user=self.user,
                country="Romania",
                postcode=574479,
                region="Timis",
                city="Timisoara",
                street="Gheorghe Lazar",
                number="24 A"
            ),
            is_active=True,
        )

        res = self.client.get(SHOP_URL)
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_shop_successful(self):
        """Test creating a Shop is successful"""
        address = sample_address()
        payload = {'name': 'ABC Corner', 'address': address.id}
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
        shop = Shop.objects.create(
            user=self.user,
            name='ABC Corner',
            address=sample_address()
        )

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
            'products': [product1.id, product2.id],
            'address': sample_address().id
        }

        res = self.client.post(SHOP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        shop = Shop.objects.get(id=res.data['id'])
        products = shop.products.all()

        self.assertEqual(len(products), 2)
        self.assertIn(product1, products)
        self.assertIn(product2, products)

    def test_retrieve_addresses(self):
        """Test retrieving addresses"""
        Address.objects.create(
            user=self.user,
            country="Romania",
            postcode=574479,
            region="Timis",
            city="Timisoara",
            street="Gheorghe Lazar",
            number="24 A"
        )

        Address.objects.create(
            user=self.user,
            country="Romania",
            postcode=574479,
            region="Cluj",
            city="Cluj-Napoca",
            street="Eroilor",
            number="123 B"
        )

        res = self.client.get(ADDRESS_URL)

        serializer = AddressSerializer(res.data, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_cerate_address_successful(self):
        """Test creating an Address is successful"""
        payload = {
            'country': 'Romania',
            'postcode': 123456,
            'region': 'Hunedoara',
            'city': 'Deva',
            'street': 'Meziad',
            'number': '12'
        }

        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Address.objects.filter(
            user=self.user, city=payload['city']
        ).exists()

        self.assertTrue(exists)

    def test_create_address_invalid(self):
        """Test creating an Address with invalid payload"""
        payload = {'country': ''}
        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_address_detail(self):
        """Test viewing Address detail"""
        address = Address.objects.create(
            user=self.user,
            country="USA",
            postcode=574479,
            region="Nevada",
            city="Las Vegas",
            street="Louis Ave",
            number="123 B"
        )

        res = self.client.get(address_detail_url(address.id))
        serializer = AddressSerializer(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
