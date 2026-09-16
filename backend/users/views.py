from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from .permissions import IsCompanyAdmin

# Create your views here.

class UserViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_system_admin:
            return User.objects.all()
        return User.objects.filter(company=self.request.user.company)
    serializer_class = UserSerializer
    permission_classes = [IsCompanyAdmin]

