from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from .permissions import IsCompanyAdmin
from rest_framework.permissions import AllowAny


# Create your views here.

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        
        if self.request.user.is_system_admin:
            return User.objects.all()
        return User.objects.filter(company=self.request.user.company)

    # check the action the user is trying to perform
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsCompanyAdmin()]



