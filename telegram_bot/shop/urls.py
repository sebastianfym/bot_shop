from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ShopViewSet, subscribe_approved, FAQViewSet, subscribe_approved_channels

router = DefaultRouter()

router.register("shop", ShopViewSet, basename="shop")
router.register("faq", FAQViewSet, basename="faq")
urlpatterns = [
                path('<int:pk>/subscribe_approved/', subscribe_approved, name='subscribe_approved'),
                path('subscribe_approved_channels/', subscribe_approved_channels, name='subscribe_approved_channels'),
              ]
urlpatterns.extend(router.urls)
