from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, InventoryViewSet, StockTransactionViewSet

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename='category')
router.register(r"products", ProductViewSet, basename='product')
router.register(r"inventories", InventoryViewSet, basename='inventory')
router.register(r"stock_transactions", StockTransactionViewSet, basename='stock_transaction')


urlpatterns = router.urls

