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


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'quantity', 'price',
                  'barcode', 'is_active', 'updated_at', 'created_at')
        read_only_fields = ('id',)
