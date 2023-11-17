from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """Is the current user a superuser."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_superuser)
