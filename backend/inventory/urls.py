from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, InventoryViewSet, StockTransactionViewSet, ProductTypeView, UnitTypeView
from django.urls import path, include

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename='category')
router.register(r"products", ProductViewSet, basename='product')
router.register(r"inventories", InventoryViewSet, basename='inventory')
router.register(r"stock_transactions", StockTransactionViewSet, basename='stock_transaction')


urlpatterns = [
    path("", include(router.urls)),
    path("product_type/", ProductTypeView.as_view()),
    path("unit_type/", UnitTypeView.as_view())
]