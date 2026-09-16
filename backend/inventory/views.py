from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializers

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers