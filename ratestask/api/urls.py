from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PortViewSet, PriceViewSet, RegionViewSet

router = DefaultRouter()
router.register(r'ports', PortViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'rates', PriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
