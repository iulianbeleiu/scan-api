from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ShopViewSet


router = DefaultRouter()
router.register('shops', ShopViewSet)

app_name = 'shop'

urlpatterns = [
    path('', include(router.urls))
]
