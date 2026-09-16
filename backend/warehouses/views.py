from rest_framework.viewsets import ModelViewSet
from .models import Warehouse
from .serializers import WarehouseSerializer

# Create your views here.
class WarehouseViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_system_admin:
            return Warehouse.objects.all()
        return Warehouse.objects.filter(company=self.request.user.company)

    serializer_class = WarehouseSerializer
