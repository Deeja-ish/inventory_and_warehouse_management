from .views import CompanyViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename='company')

urlpatterns = router.urls

