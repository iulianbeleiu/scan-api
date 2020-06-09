from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ShopViewSet, ProductViewSet, CartView


router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductViewSet)

app_name = 'shop'

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart')
]
