from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


# old permission
class IsVerifPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_verif:
            raise PermissionDenied("У вас не активований акаунт")
        return user.is_verif
