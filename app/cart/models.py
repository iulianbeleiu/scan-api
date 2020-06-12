from django.db import models
from django.conf import settings


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField(CartItem)
    total = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
