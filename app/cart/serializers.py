from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart item objects"""

    class Meta:
        model = CartItem
        fields = ('id', 'name', 'price', 'quantity', 'user')
        read_only_fields = ('id', 'user')
