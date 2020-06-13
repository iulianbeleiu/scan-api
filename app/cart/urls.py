from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CartItemViewSet, CartViewSet


router = DefaultRouter()
router.register('items', CartItemViewSet)
router.register('cart', CartViewSet)

app_name = 'cart'

urlpatterns = [
    path('', include(router.urls))
]
