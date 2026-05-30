from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

class ForceReauthMiddleware:
    """
    Middleware qui force la reconnexion à chaque chargement de page
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Liste des URLs autorisées sans authentification
        allowed_urls = ['/login/', '/register/', '/admin/']
        
        # Vérifier si l'utilisateur est connecté
        if request.user.is_authenticated:
            # Vérifier si la session est encore valide
            if not request.session.exists(request.session.session_key):
                logout(request)
                return redirect('login')
            
            # Ajouter un header anti-cache
            response = self.get_response(request)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        
        # Si l'utilisateur n'est pas connecté et essaie d'accéder à une page protégée
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in allowed_urls):
            if request.path != '/':
                return redirect('login')
        
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response