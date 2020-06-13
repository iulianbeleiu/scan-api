from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

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
        queryset = self.queryset.filter(user=self.request.user)\
            .order_by('updated_at')
        cart_items = []
        if self.request.session.get('cart_items'):
            cart_items = self.request.session['cart_items']
        return queryset.filter(user=self.request.user, pk__in=cart_items)

    def perform_create(self, serializer):
        """Create a new object for current user"""
        cart_item = serializer.save(user=self.request.user)
        if self.request.session.get('cart_items'):
            cart_items = self.request.session['cart_items']
            cart_items.append(cart_item.id)
            self.request.session['cart_items'] = cart_items
        else:
            self.request.session['cart_items'] = [cart_item.id]


class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)
