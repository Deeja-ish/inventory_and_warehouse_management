from rest_framework.viewsets import ModelViewSet
from .models import Warehouse
from .serializers import WarehouseSerializer
from .permission  import IsAllowed
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsManagerOrAdmin
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

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
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

    # create the warehouse summary count
    @action(detail=False, methods=['get'])
    def summary(self, request):
        warehouse = self.get_queryset()

        summary = warehouse.aggregate(
            total_warehouse = Count("id")
        )
        return Response(summary)


# show the warehouse type options
class WarehouseTypeView(APIView):
    def get(self, request):
        types_warehouse = Warehouse.WarehouseType.choices 
        return Response(types_warehouse)


# create a view for the capacity_unit
class CapacityUnitView(APIView):
    def get(self, request):
        types_capacity = Warehouse.CapacityUnit.choices
        return Response(types_capacity)


    

