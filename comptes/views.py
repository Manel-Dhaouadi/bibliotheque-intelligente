from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Utilisateur

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not username or not email or not password1:
            messages.error(request, "Tous les champs sont obligatoires")
            return render(request, 'auth/register.html')
        
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, 'auth/register.html')
        
        if len(password1) < 6:
            messages.error(request, "Le mot de passe doit contenir au moins 6 caractères")
            return render(request, 'auth/register.html')
        
        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé")
            return render(request, 'auth/register.html')
        
        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris")
            return render(request, 'auth/register.html')
        
        try:
            Utilisateur.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role='client'
            )
            messages.success(request, "✅ Compte créé avec succès ! Connectez-vous")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return render(request, 'auth/register.html')
    
    return render(request, 'auth/register.html')

def login_view(request):
    # Si déjà connecté, rediriger vers accueil
    if request.user.is_authenticated:
        return redirect('accueil')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Veuillez saisir votre email et mot de passe")
            return render(request, 'auth/login.html')
        
        try:
            user_obj = Utilisateur.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Bonjour {user.username} !")
                # Redirection explicite vers accueil
                return redirect('accueil')
            else:
                messages.error(request, "Email ou mot de passe incorrect")
        except Utilisateur.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect")
        
        return render(request, 'auth/login.html')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté")
    return redirect('login')