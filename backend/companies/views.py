from rest_framework.viewsets import ModelViewSet
from .serializers import CompanySerializer
from .models import Company

# Create your views here.
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer