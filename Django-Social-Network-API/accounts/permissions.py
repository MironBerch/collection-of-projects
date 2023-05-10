from rest_framework.permissions import BasePermission


class IsUserProfileOwner(BasePermission):
    """
    Check if user is owner of the profile.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user or request.user.is_staff
        )
