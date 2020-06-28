from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Anyline
from .serializers import AnylineSerializer


class AnylineViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Anyline.objects.all()
    serializer_class = AnylineSerializer

    def perform_create(self, serializer):
        """Create a new object for current user"""
        serializer.save(user=self.request.user)
