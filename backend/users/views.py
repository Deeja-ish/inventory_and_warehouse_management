from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer, UserDisplayProfileView, ChangePasswordSerializer, LogoutSerializer
from .permissions import IsManagerOrAdmin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from rest_framework.decorators import action 


# Create your views here.
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        
        if self.request.user.is_system_admin:
            return User.objects.all()
        
        if self.request.user.role in [User.Role.ADMIN, User.Role.MANAGER]:
            if not self.request.user.company:
                return User.objects.none()
            return User.objects.filter(company=self.request.user.company)
        return User.objects.filter(id=self.request.user.id)
        
    # check the action the user is performing
    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), IsManagerOrAdmin()]

    # create a custome action to all role updating 
    @action(detail=True, methods=['patch'])
    def update_role(self, request, pk=None):
        target_user = self.get_object()
        # get the updated row
        new_role = request.data.get("role")
        if not new_role:
            return Response({
                "message" : "New role must be included"
            }, status=status.HTTP_400_BAD_REQUEST)
        # check if the users role is system_admin or manager
        is_system_admin = getattr(request.user, "is_system_admin", False) or request.user.is_superuser
        if not is_system_admin:
            if request.user.company != target_user.company:
                return Response({
                    "message" : "You do not have permission to perform this action"
                }, status=status.HTTP_403_FORBIDDEN)

        # ensure a user cannot update his row 
        if request.user == target_user:
            return Response({
                "message" : "You can not update your own role"
            }, status=status.HTTP_400_BAD_REQUEST)

        # check the roles that are allowed to be updated
        allowed_roles = []
        if is_system_admin:
            allowed_roles = [User.Role.ADMIN, User.Role.AUDITOR, User.Role.STAFF, User.Role.MANAGER, User.Role.STORE_KEEPER]
        elif request.user.role == User.Role.ADMIN:
            allowed_roles = [User.Role.STORE_KEEPER, User.Role.STAFF, User.Role.AUDITOR, User.Role.MANAGER, User.Role.ADMIN]
        elif request.user.role == User.Role.MANAGER:
            allowed_roles = [User.Role.AUDITOR, User.Role.STAFF, User.Role.STORE_KEEPER]
        
        # check if the new role is allowed to be updated
        if new_role not in allowed_roles:
            return Response({
                "message" : "Invalid Role"
            }, status=status.HTTP_400_BAD_REQUEST)
        # Save and update the role
        target_user.role = new_role
        target_user.save()
        return Response({"message" : "User Role and been updated successfully"}, status=status.HTTP_200_OK)

            


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


# get a list of users category 
class GetRolesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_category = User.Role.choices
        return Response(user_category, status=status.HTTP_200_OK)
