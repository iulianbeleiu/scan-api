from django.db import models
from django.conf import settings


class Shop(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
