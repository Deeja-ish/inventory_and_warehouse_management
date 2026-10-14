from rest_framework.viewsets import ModelViewSet
from .serializers import CompanySerializer, CompanyListSerializer
from .models import Company
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 

# Create your views here.
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer

# get the companies to diplay in the frontend 
class CompanyList(APIView):
    def get(self, request):
        company = Company.objects.filter(is_active=True)
        serializer = CompanyListSerializer(company, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)