from rest_framework.viewsets import ModelViewSet
from .models import Warehouse
from .serializers import WarehouseSerializer
from .permission  import IsAllowed
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsManagerOrAdmin
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response

# Create your views here.
class WarehouseViewSet(ModelViewSet):
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        if self.request.user.is_system_admin:
            return Warehouse.objects.all()
        return Warehouse.objects.filter(company=self.request.user.company)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        if self.action in ['create', "update", "partial_update"]:
            return [IsAllowed()]
        if self.action == 'destroy':
            return [IsCompanyAdmin()]
        return [AllowAny()]

    # create the warehouse summary count
    @action(detail=False, methods=['get'])
    def summary(self, request):
        warehouse = self.get_queryset()

        summary = warehouse.aggregate(
            total_warehouse = Count("id")
        )
        return Response(summary)

