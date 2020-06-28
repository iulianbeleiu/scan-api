from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from anyline.models import Anyline
from anyline.serializers import AnylineSerializer


ANYLINE_URL = reverse('anyline:anyline-list')


def sample_user():
    """Create sample user"""
    return get_user_model().objects.create(
        email='test@test.com',
        password='test123'
    )


class PrivateAnylineTests(TestCase):
    """Test that Anyline API is not publicly available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_for_anyline(self):
        """Test that login is required"""

        res = self.client.get(ANYLINE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicAnylineTests(TestCase):
    """Test the authorized Anyline API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='sample@test.com',
            password='sample123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_anyline(self):
        """Test retrieving anyline licence"""
        Anyline.objects.create(
            user=self.user,
            name='dev',
            licence_text='blablabla',
            active=True,
        )

        res = self.client.get(ANYLINE_URL)
        anyline = Anyline.objects.all()
        serializer = AnylineSerializer(anyline, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_allowed_create_anyline(self):
        """Test that creating anyline is not possible"""
        payload = {
            'name': 'Test',
            'license_text': 'blabla',
            'active': True,
        }

        res = self.client.post(ANYLINE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
