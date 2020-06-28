from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnylineViewSet

router = DefaultRouter()
router.register('anyline', AnylineViewSet)

app_name = 'anyline'

urlpatterns = [
    path('', include(router.urls))
]
