from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You do not have permission to access this user'

    def has_permission(self, request, view):
        requested_user_id = view.kwargs.get('pk')
        return request.user.id == requested_user_id
