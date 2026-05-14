from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permission pour les administrateurs uniquement.
    Vérifie que l'utilisateur est connecté ET a le rôle 'admin'.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

class IsClientUser(permissions.BasePermission):
    """
    Permission pour les clients uniquement.
    Vérifie que l'utilisateur est connecté ET a le rôle 'client'.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'client'
        )

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Lecture publique, écriture seulement pour utilisateurs connectés.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated