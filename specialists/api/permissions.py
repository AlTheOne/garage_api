from rest_framework import permissions


class SpecialistPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            if not request.user.is_authenticated:
                return False

            return request.user.has_perm('specialists.add_specialist')

        return True

    def has_object_permission(self, request, view, obj):
        if view.action in {'update', 'partial_update'}:
            if not request.user.is_authenticated:
                return False

            return request.user.has_perm('specialists.change_specialist')

        if view.action == 'destroy':
            if not request.user.is_authenticated:
                return False

            return request.user.has_perm('specialists.delete_specialist')

        return True
