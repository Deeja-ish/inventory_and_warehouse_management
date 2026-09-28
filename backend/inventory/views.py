from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Inventory, StockTransaction
from .serializers import CategorySerializers, ProductSerializer, InventorySerializer, StockTransactionSerializer
from .permission import IsAllowedAdmin, IsProductManager, IsStockManager
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompanyAdmin
from rest_framework.decorators import action
from django.db.models import F, Sum, Count, Q, models 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

# Create your views here.
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializers

    def get_queryset(self):
        if self.request.user.is_system_admin:
            return Category.objects.all()
        return Category.objects.filter(company=self.request.user.company)

    def get_permissions(self):
        # check if its system admin
        if self.action in ['list', 'retrieve']:
            return[IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update']:
            return[IsAllowedAdmin()]
        if self.action == 'destroy':
            return[IsCompanyAdmin()]
        return[IsAuthenticated()]
    


# create the views for the product
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
        # check if the user is authenticated
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        # check it the user is system admin
        if self.request.user.is_system_admin:
            return Product.objects.all()
        return Product.objects.filter(company=self.request.user.company)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update']:
            return [IsProductManager()]
        if self.action == 'destroy':
            return [IsCompanyAdmin()]
        return [IsAuthenticated()]

class InventoryViewSet(ModelViewSet):
    serializer_class = InventorySerializer
    http_method_names = ['get']

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "warehouse"]
        
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Inventory.objects.none()
        if self.request.user.is_system_admin:
            return Inventory.objects.all()
        return Inventory.objects.filter(product__company= self.request.user.company)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        inventory = self.get_queryset().filter(
            available_quantity__Ite=F("reorder_level")
        )
        serializer = self.get_serializer(inventory, many=True)

        return Response(serializer.data)



class StockTransactionViewSet(ModelViewSet):
    serializer_class = StockTransactionSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['products', "warehouse", 'transaction_type']

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return StockTransaction.objects.none()
        if self.request.user.is_system_admin:
            return StockTransaction.objects.all()
        return StockTransaction.objects.filter(product__company=self.request.user.company)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return[IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update']:
            return[IsStockManager()]
        if self.action == "destroy":
            return [IsCompanyAdmin()]
        return [IsAuthenticated()]

    # create a summary to return the aggregrate of all transactions
    @action(detail=False, methods=["get"])
    def summary(self, request):
        transactions = self.get_queryset()

        summary = transactions.aggregate(
            total_transaction = Count("id"),

            total_received = Sum("quantity", filter=models.Q(
                StockTransaction.TransactionType.RECIEVE
            )),
            total_issued = Sum("quantity", filter=models.Q(
                StockTransaction.TransactionType.ISSUE
            )),
            total_adjustment = Sum("quantity", filter=models.Q(
                StockTransaction.TransactionType.ADJUSTMENT
            )),
            total_return = Sum("quantity", filter=models.Q(
                StockTransaction.TransactionType.RETURN 
            ))
        )

        
        return Response(summary)

    
    
