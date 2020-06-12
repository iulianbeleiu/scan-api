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

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name
