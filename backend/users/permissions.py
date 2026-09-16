from rest_framework.permissions import BasePermission

class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and ( request.user.is_system_admin or request.user.role == request.user.Role.ADMIN))