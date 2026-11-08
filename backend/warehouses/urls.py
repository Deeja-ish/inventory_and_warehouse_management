from .views import WarehouseViewSet, WarehouseTypeView, CapacityUnitView
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()

router.register(r"warehouses", WarehouseViewSet, basename="warehouse")

urlpatterns = [
    path("", include(router.urls)),
    path("warehouse_types/", WarehouseTypeView.as_view()),
    path("capacity_types/", CapacityUnitView.as_view())
]