from rest_framework import serializers

from .models import Shop, Product


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for shop objects"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Shop
        fields = ('id', 'user', 'name', 'is_active', 'products')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = ('id', 'user', 'name', 'description', 'quantity', 'price',
                  'barcode', 'is_active', 'image', 'updated_at', 'created_at')
        read_only_fields = ('id',)


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to products"""

    class Meta:
        model = Product
        fields = ('id', 'image')
        read_only_fields = ('id',)
