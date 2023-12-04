from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import Authentication

router = DefaultRouter()

router.register("authentication", Authentication)

urlpatterns = router.urls