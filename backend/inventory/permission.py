from rest_framework.permissions import BasePermission
from users.models import User

class IsAllowedAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        allowed_host = [
            User.Role.ADMIN,
            User.Role.MANAGER,
            User.Role.STORE_KEEPER
        ]

        return request.user.role in allowed_host

class IsProductManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        allowed_host = [
            User.Role.ADMIN,
            User.Role.MANAGER,
            User.Role.STORE_KEEPER
        ]

        return request.user.role in allowed_host
