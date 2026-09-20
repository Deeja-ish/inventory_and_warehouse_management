from rest_framework.permissions import BasePermission

class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # allow system admins and superusers to have access
        if getattr(request.user, 'is_system_admin', False) or request.user.is_superuser:
            return True

        return request.user.role == request.user.Role.ADMIN