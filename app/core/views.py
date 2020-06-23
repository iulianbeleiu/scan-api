from rest_framework.decorators import api_view, \
                                     permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request, format=None):
    return Response({
        'user-create': reverse('user:create',
                               request=request, format=format),
        'user-token': reverse('user:token',
                              request=request, format=format),
        'user-me': reverse('user:me',
                           request=request, format=format),
        'shops': reverse('shop:shop-list',
                         request=request, format=format),
        'address': reverse('shop:address-list',
                           request=request, format=format),
        'products': reverse('shop:product-list',
                            request=request, format=format),
        'cart': reverse('cart:cart-list',
                        request=request, format=format),
        'cart-items': reverse('cart:cartitem-list',
                              request=request, format=format),
    })


@api_view(['GET'])
def ping(request, format=None):
    return Response('Ok')
