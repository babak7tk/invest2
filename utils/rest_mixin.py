from rest_framework import permissions


class RestPermissionMixin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if not hasattr(view, 'permissions'):
            return True
        for permission in view.permissions:
            if any(permission in p for p in request.user.permissions):
                return True
        return False
