from rest_framework import serializers
from .models import Anyline


class AnylineSerializer(serializers.ModelSerializer):
    """Serializer for anyline objects"""

    class Meta:
        model = Anyline
        fields = '__all__'
        read_only_fields = ('id', 'user')
