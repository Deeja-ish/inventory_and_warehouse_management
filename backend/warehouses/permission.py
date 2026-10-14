from rest_framework.permissions import BasePermission
from users.models import User

class IsAllowed(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        allowed_roles = [
            User.Role.ADMIN,
            User.Role.MANAGER, 
            User.Role.STORE_KEEPER
        ]

        return request.user.role in allowed_roles