from .views import CompanyViewSet, CompanyList
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename='company')

urlpatterns = [
    path("", include(router.urls)),
    path("list_company/", CompanyList.as_view(), name='list_companies')
]

