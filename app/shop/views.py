from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Shop, Product

from .serializers import ShopSerializer, ProductSerializer, \
                            ProductImageSerializer


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

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return ProductImageSerializer

        return self.serializer_class

    @action(methods=['GET'], detail=False,
            url_path='barcode/(?P<barcode>[^/.]+)')
    def barcode(self, request, barcode=None):
        """Get a shop product by product barcode"""

        product = get_object_or_404(Product, barcode=barcode)
        serializer = ProductSerializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a product"""
        product = self.get_object()
        serializer = self.get_serializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
