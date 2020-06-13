from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ShopViewSet, ProductViewSet


router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductViewSet)

app_name = 'shop'

urlpatterns = [
    path('', include(router.urls)),
]
