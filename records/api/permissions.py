from rest_framework import permissions


class RecordPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Возможно удалать только свои заявки...
        if view.action == 'destroy':
            return obj.created_by == request.user

        return True
