from rest_framework import serializers
from .models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart item objects"""

    class Meta:
        model = CartItem
        fields = ('id', 'name', 'price', 'quantity', 'user')
        read_only_fields = ('id', 'user')


class CartSerializer(serializers.ModelSerializer):
    """Serializer for cart objects"""

    items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CartItem.objects.all()
    )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ('id',)
