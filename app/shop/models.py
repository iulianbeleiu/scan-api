import uuid
import os

from django.db import models
from django.conf import settings


def product_image_file_path(instance, filename):
    """Generate file path for new product image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/product/', filename)


class Shop(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField('Product')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()
    barcode = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, upload_to=product_image_file_path)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
