from rest_framework import permissions

"""IsAdminOrSuperUser IsSuperUser IsAdmin это для работы с users,
GTC это для категорий, жанров и тайтлов, насколько я понял
это админ работает остальные только читают.
AOM это для оценок и комментариев """


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == 'admin'


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin')


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'moderator')


class GTC(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            (request.user.is_authenticated and (
                request.user.is_superuser or request.user.role == 'admin')))


class AOM(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or (
            request.user.role == 'admin',
            request.user.role == 'moderator')
