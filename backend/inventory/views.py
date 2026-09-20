from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Inventory, StockTransaction
from .serializers import CategorySerializers, ProductSerializer, InventorySerializer, StockTransactionSerializer
from .permission import IsAllowedAdmin, IsProductManager
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompanyAdmin

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
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Inventory.objects.none()
        return Inventory.objects.filter(product__company= self.request.user.company)
    serializer_class = InventorySerializer
    http_method_names = ['get']

class StockTransactionViewSet(ModelViewSet):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return StockTransaction.objects.none()
        return StockTransaction.objects.filter(user=self.request.user, product=self.request.user.products, product__company=self.request.user.company)
    serializer_class = StockTransactionSerializer


# {
#   "username" : "manager5",
#   "first_name" : "hassan",
#   "last_name" : "bashir",
#   "email" : "hassan@gmail.com",
#   "password" : "Bashir12345",
#   "confirm_password" : "Bashir12345",
#   "company" : 4,
#   "role" : "Manager",
#   "phone_number" :"0908765477566"
# }