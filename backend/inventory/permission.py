from rest_framework.permissions import BasePermission
from users.models import User


# create the login permission
class IsAllowedAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if getattr(request.user, "is_system_admin", False):
            return True
        allowed_host = [
            User.Role.ADMIN,
            User.Role.MANAGER,
            User.Role.STORE_KEEPER

        ]
        return request.user.role in allowed_host 