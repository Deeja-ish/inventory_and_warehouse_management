from rest_framework.viewsets import ModelViewSet
from .serializers import CompanySerializer, CompanyListSerializer
from .models import Company
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from users.permissions import IsSystemAdmin, IsCompanyAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.
class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        companies = Company.objects.filter(is_active=True)
        if not user.is_authenticated:
            return companies.none
        if user.is_superuser or user.is_system_admin:
            return companies
        return companies.filter(id=user.company_id)

    def get_permission(self):
        if(self.action == 'create'):
            return [AllowAny()]
        if self.action in ['update', 'partial_update']:
            return [IsCompanyAdmin()]
        if self.action == 'destroy':
            return [IsSystemAdmin()]
        return [IsAuthenticated()]

# get the companies to diplay in the frontend 
class CompanyList(APIView):
    permission_classes = [AllowAny()]
    def get(self, request):
        company = Company.objects.filter(is_active=True)
        serializer = CompanyListSerializer(company, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)