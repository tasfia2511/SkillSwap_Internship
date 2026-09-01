from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    message = "Admin role required."

    def has_permission(self, request, view):

        print(
            "RBAC DEBUG:",
            request.user,
            request.user.username if request.user.is_authenticated else "Anonymous",
            getattr(
                getattr(request.user, 'profile', None),
                'role',
                'NO PROFILE'
            )
        )

        if not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.role == 'ADMIN'

        except AttributeError:
            return False

class IsModerator(BasePermission):

    message = "Moderator or Admin role required."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        try:
            role = request.user.profile.role

            return role in ['MODERATOR', 'ADMIN']

        except AttributeError:
            return False


class IsOwnerOrAdmin(BasePermission):

    message = "You can only access your own data."

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):

        if not request.user.is_authenticated:
            return False

        try:

            if request.user.profile.role == 'ADMIN':
                return True

        except AttributeError:
            pass

        return obj.user == request.user