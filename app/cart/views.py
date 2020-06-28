from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from django.template.loader import get_template
from django.http import HttpResponse

from xhtml2pdf import pisa

from .models import CartItem, Cart

from .serializers import CartItemSerializer, CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user, cart=None)\
            .order_by('updated_at')

    def perform_create(self, serializer):
        """Create a new object for current user"""
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    @action(methods=['GET'], detail=True, url_path='receipt')
    def receipt(self, request, pk=None):
        cart = self.get_object()
        pdf_name = f'receipt-{cart.id}.pdf'
        template_path = 'receipt.html'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'

        template = get_template(template_path)
        html = template.render({'cart': cart, 'user': request.user})

        pisa.CreatePDF(html, dest=response)

        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
