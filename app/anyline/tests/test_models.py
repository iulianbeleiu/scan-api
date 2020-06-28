from django.test import TestCase
from django.contrib.auth import get_user_model

from anyline.models import Anyline


class ModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='test123',
        )

    def test_create_anyline(self):
        """Test anyline string representation"""
        anyline = Anyline.objects.create(
            user=self.user,
            name='dev',
            licence_text='blablabla',
            active=True,
        )

        self.assertEqual(str(anyline), anyline.name)
