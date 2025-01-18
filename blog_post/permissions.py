from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """ Only Auhtor is allowed to create Post"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.bloguser.role == "Author"

class IsReaderOrReadOnly(BasePermission):
    """ Only Reader is allowed to add comment to the post"""
    def has_permission(self, request, view):
        return request.user.bloguser.role == 'Reader'