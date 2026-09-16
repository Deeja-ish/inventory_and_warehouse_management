from .views import WarehouseViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"warehouses", WarehouseViewSet, basename="warehouse")

urlpatterns = router.urls