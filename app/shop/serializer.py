from rest_framework import serializers

from .models import Shop, Product


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop objects"""

    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Shop
        fields = ('id', 'name', 'is_active', 'products')
        read_only_fields = ('id',)
