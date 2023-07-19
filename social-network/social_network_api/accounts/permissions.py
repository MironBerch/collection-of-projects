from rest_framework.permissions import BasePermission


class IsUserProfileOwner(BasePermission):
    """
    Check if authenticated user is owner of user profile.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsNotAuthenticated(BasePermission):
    """
    Check if user not authenticated.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is False

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated is False
