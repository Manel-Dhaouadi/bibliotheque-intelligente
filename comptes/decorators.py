from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, "Accès réservé aux administrateurs")
            return redirect('accueil')
        return view_func(request, *args, **kwargs)
    return wrapper