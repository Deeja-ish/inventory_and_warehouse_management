from rest_framework.permissions import BasePermission
from .models import User

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # allow system admins and superusers 
        if getattr(request.user, "is_system_admin", False) or request.user.is_superuser:
            return True

        return request.user.role in [User.Role.ADMIN, User.Role.MANAGER]


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        return bool(user and user.is_authenticated and (getattr(user, 'is_system_admin', False) or user.is_superuser))


# create the company admin permission
class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not(user and user.is_authenticated):
            return False
        if getattr(user, "is_system_admin", False):
            return True
        return user.role == User.Role.ADMIN

    