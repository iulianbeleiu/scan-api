from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Shop

from .serializer import ShopSerializer


class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for Shop"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

    def get_queryset(self):
        """Custom queryset for authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a Shop"""
        return serializer.save(user=self.request.user)
