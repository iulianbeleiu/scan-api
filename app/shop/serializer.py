from rest_framework import serializers

from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop objects"""

    class Meta:
        model = Shop
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id',)
