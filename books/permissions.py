from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the review
        return obj.user == request.user

class CanDeleteReview(permissions.BasePermission):
    """
    Allow deletion only to the owner or admin.
    """
    def has_object_permission(self, request, view, obj):
        # Only POST, PUT, PATCH, DELETE methods need checking
        if request.method == 'DELETE':
            return obj.user == request.user or request.user.is_staff
        return True