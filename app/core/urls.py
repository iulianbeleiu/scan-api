from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('ping', views.ping, name='ping'),
]
