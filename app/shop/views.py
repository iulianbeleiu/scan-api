from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Shop

from .serializer import ShopSerializer


class ShopViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ViewSet for Shop"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

    def get_queryset(self):
        """Custom queryset for authenticated user"""
        return self.queryset.filter(user=self.request.user)
