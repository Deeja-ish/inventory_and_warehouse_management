from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Inventory, StockTransaction
from .serializers import CategorySerializers, ProductSerializer, InventorySerializer, StockTransactionSerializer
from .permission import IsAllowedAdmin, IsProductManager, IsStockManager, IsInventoryManager
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsManagerOrAdmin
from rest_framework.decorators import action
from django.db.models import F, Sum, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db import models
from rest_framework.views import APIView
from rest_framework import status

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
            return[IsInventoryManager()]
        if self.action == 'destroy':
            return[IsManagerOrAdmin()]
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
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

    # create a route to get the summary of products
    @action(detail=False, methods=['get'])
    def summary(self, request):
        products = self.get_queryset()
        # get the totalproducts of that company 
        summary = products.aggregate(
            total_products = Count("id")
        )
        return Response(summary)

# get the product types
class ProductTypeView(APIView):
    def get(self, request):
        product_types = Product.ProductType.choices
        return Response(product_types, status=status.HTTP_200_OK)

# get the unit types
class UnitTypeView(APIView):
    def get(self, request):
        unit_types = Product.UnitType.choices
        return Response(unit_types, status=status.HTTP_200_OK)
    

class InventoryViewSet(ModelViewSet):
    serializer_class = InventorySerializer
    http_method_names = ['get', "patch"]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "warehouse"]
        
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Inventory.objects.none()
        if self.request.user.is_system_admin:
            return Inventory.objects.all()
        return Inventory.objects.filter(product__company= self.request.user.company)

    def get_permissions(self):
        if self.action == ['partial_update']:
            return [IsInventoryManager()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        inventory = self.get_queryset().filter(
            available_quantity__lte=F("reorder_level")
        )
        serializer = self.get_serializer(inventory, many=True)

        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def summary(self, request):
        inventory = self.get_queryset()

        summary = inventory.aggregate(
            total_inventory = Count('id')
        )

        return Response(summary)


class StockTransactionViewSet(ModelViewSet):
    serializer_class = StockTransactionSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', "warehouse", 'transaction_type']

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
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

    # create a summary to return the aggregrate of all transactions
    @action(detail=False, methods=["get"])
    def summary(self, request):
        transactions = self.get_queryset()

        summary = transactions.aggregate(
            total_transaction = Count("id"),

            total_received = Sum("quantity", filter=models.Q(
                transaction_type = StockTransaction.TransactionType.RECIEVE
            )),
            total_issued = Sum("quantity", filter=models.Q(
                transaction_type=StockTransaction.TransactionType.ISSUE
            )),
            total_adjustment = Sum("quantity", filter=models.Q(
                transaction_type=StockTransaction.TransactionType.ADJUSTMENT
            )),
            total_return = Sum("quantity", filter=models.Q(
                transaction_type=StockTransaction.TransactionType.RETURN 
            ))
        )
        return Response(summary)


    