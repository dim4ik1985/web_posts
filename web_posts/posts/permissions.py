from rest_framework.permissions import BasePermission

# Разрешения для пользователя
class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


# Разрешения для поста и комментария
class IsAdminOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user
