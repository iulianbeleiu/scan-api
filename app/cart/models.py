from django.db import models
from django.conf import settings

from shop.models import Shop


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
    class Meta:
        verbose_name_plural = "Cart"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField(CartItem)
    total = models.FloatField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    completed = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)
