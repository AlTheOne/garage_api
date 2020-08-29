from rest_framework import permissions


class RegistrationPermission(permissions.BasePermission):
    """
    Только неавторизованные пользователи.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return False

        return True
