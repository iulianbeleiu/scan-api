from rest_framework.decorators import action
from rest_framework import viewsets, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Shop, Product

from .serializer import ShopSerializer, ProductSerializer, \
                            ProductImageSerializer, CartSerializer


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

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return ProductImageSerializer

        return self.serializer_class

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


class CartView(generics.RetrieveUpdateAPIView):
    """ViewSet for Cart"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def retrieve(self, request, *args, **kwargs):
        """Get cart from session"""
        if request.session.get('cart', False):
            return Response(request.session['cart'], status=status.HTTP_200_OK)

        return Response([])

    def update(self, request, *args, **kwargs):
        """Update or Create cart in session"""
        serializer = CartSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data

                product = data['products']
                quantity = data['quantity']
                if quantity > product.quantity:
                    message = {
                        "quantity": [
                            "Quantity too high."
                        ]
                    }
                    return Response(message,
                                    status=status.HTTP_400_BAD_REQUEST)

                total = product.price * quantity

                if 'cart' in self.request.session:
                    cart = self.request.session['cart']
                    cart['products'].append(product.id)
                    cart['total'] += total
                    self.request.session['cart'] = cart
                else:
                    cart = {
                        'total': total,
                        'products': [product.id]
                    }
                    self.request.session['cart'] = cart
                return Response(cart, status=status.HTTP_200_OK)
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
