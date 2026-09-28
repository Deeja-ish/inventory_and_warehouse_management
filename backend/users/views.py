from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer, UserDisplayProfileView, ChangePasswordSerializer, LogoutSerializer
from .permissions import IsCompanyAdmin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 

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


# create the profile viewset
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserDisplayProfileView(user)

        return Response(serializer.data)

# create a change password view
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user 
        serializer = ChangePasswordSerializer(user)

        if serializer.is_valid():
            new_password = serializer.validated_data.get(new_password)
            # set the new password 
            user.set_password(new_password)
            user.save()

            return Response({
                "message" : "Password reset Successfully",
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# create the logout view 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Logout has been Successful"}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


