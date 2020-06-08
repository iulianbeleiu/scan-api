from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Shop, Product

from .serializer import ShopSerializer, ProductSerializer


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


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        """Custom queryset for authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a Product"""
        return serializer.save(user=self.request.user)

    @action(methods=['GET'], detail=False,
            url_path='barcode/(?P<barcode>[^/.]+)')
    def barcode(self, request, barcode=None):
        """Get a shop product by product barcode"""

        product = get_object_or_404(Product, barcode=barcode)
        serializer = ProductSerializer(product)

        return Response(
            serializer.data,
            status=200
        )
