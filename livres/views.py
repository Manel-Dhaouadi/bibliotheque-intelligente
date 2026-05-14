from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Livre, Categorie, Emprunt
from .services.chatbot_service import ChatbotService
from comptes.decorators import admin_required
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@login_required
def accueil(request):
    """Page d'accueil - nécessite connexion"""
    total_livres = Livre.objects.count()
    livres_disponibles = Livre.objects.filter(quantite_disponible__gt=0).count()
    emprunts_actifs = Emprunt.objects.filter(date_retour_reelle__isnull=True).count()
    taux = (livres_disponibles / total_livres * 100) if total_livres > 0 else 0
    
    derniers_livres = Livre.objects.select_related('categorie').all().order_by('-date_ajout')[:6]
    
    context = {
        'total_livres': total_livres,
        'livres_disponibles': livres_disponibles,
        'taux_disponibilite': round(taux),
        'emprunts_actifs': emprunts_actifs,
        'derniers_livres': derniers_livres,
    }
    return render(request, 'accueil.html', context)

@login_required
def liste_livres(request):
    """Liste des livres - nécessite connexion"""
    livres = Livre.objects.select_related('categorie').all()
    return render(request, 'livres/liste.html', {'livres': livres})

@login_required
@admin_required
def ajouter_livre(request):
    """Ajouter un livre - admin uniquement"""
    if request.method == 'POST':
        livre = Livre.objects.create(
            titre=request.POST.get('titre'),
            auteur=request.POST.get('auteur'),
            categorie_id=request.POST.get('categorie') or None,
            annee_publication=request.POST.get('annee_publication') or None,
            quantite_totale=int(request.POST.get('quantite_totale', 1)),
            quantite_disponible=int(request.POST.get('quantite_disponible', 1)),
        )
        messages.success(request, f'Livre "{livre.titre}" ajouté avec succès')
        return redirect('liste_livres')
    
    categories = Categorie.objects.all()
    return render(request, 'livres/ajouter.html', {'categories': categories})

@login_required
@admin_required
def modifier_livre(request, pk):
    """Modifier un livre - admin uniquement"""
    livre = get_object_or_404(Livre, id_livre=pk)
    
    if request.method == 'POST':
        livre.titre = request.POST.get('titre')
        livre.auteur = request.POST.get('auteur')
        livre.categorie_id = request.POST.get('categorie') or None
        livre.annee_publication = request.POST.get('annee_publication') or None
        livre.quantite_totale = int(request.POST.get('quantite_totale', 1))
        livre.quantite_disponible = int(request.POST.get('quantite_disponible', 1))
        livre.save()
        messages.success(request, f'Livre "{livre.titre}" modifié avec succès')
        return redirect('liste_livres')
    
    categories = Categorie.objects.all()
    return render(request, 'livres/modifier.html', {'livre': livre, 'categories': categories})

@login_required
@admin_required
def supprimer_livre(request, pk):
    """Supprimer un livre - admin uniquement"""
    livre = get_object_or_404(Livre, id_livre=pk)
    
    if request.method == 'POST':
        titre = livre.titre
        livre.delete()
        messages.success(request, f'Livre "{titre}" supprimé avec succès')
        return redirect('liste_livres')
    
    return render(request, 'livres/supprimer.html', {'livre': livre})

@login_required
def emprunter_livre(request, pk):
    """Emprunter un livre - nécessite connexion"""
    livre = get_object_or_404(Livre, id_livre=pk)
    
    if livre.quantite_disponible <= 0:
        messages.error(request, "Ce livre n'est pas disponible")
        return redirect('liste_livres')
    
    livre.quantite_disponible -= 1
    livre.save()
    
    Emprunt.objects.create(
        livre=livre,
        utilisateur=request.user,
        utilisateur_nom=request.user.username
    )
    
    messages.success(request, f'✓ Livre "{livre.titre}" emprunté avec succès. Retour prévu dans 5 jours.')
    return redirect('liste_livres')

@login_required
@admin_required
def liste_categories(request):
    """Liste des catégories - admin uniquement"""
    categories = Categorie.objects.annotate(nb_livres=Count('livres'))
    return render(request, 'categories/liste.html', {'categories': categories})

@login_required
@admin_required
def ajouter_categorie(request):
    """Ajouter une catégorie - admin uniquement"""
    if request.method == 'POST':
        categorie = Categorie.objects.create(
            nom=request.POST.get('nom'),
            description=request.POST.get('description')
        )
        messages.success(request, f'Catégorie "{categorie.nom}" ajoutée avec succès')
        return redirect('liste_categories')
    
    return render(request, 'categories/ajouter.html')

@login_required
@admin_required
def modifier_categorie(request, pk):
    """Modifier une catégorie - admin uniquement"""
    categorie = get_object_or_404(Categorie, id=pk)
    
    if request.method == 'POST':
        categorie.nom = request.POST.get('nom')
        categorie.description = request.POST.get('description')
        categorie.save()
        messages.success(request, f'Catégorie "{categorie.nom}" modifiée avec succès')
        return redirect('liste_categories')
    
    return render(request, 'categories/modifier.html', {'categorie': categorie})

@login_required
@admin_required
def supprimer_categorie(request, pk):
    """Supprimer une catégorie - admin uniquement"""
    categorie = get_object_or_404(Categorie, id=pk)
    
    if categorie.livres.count() > 0:
        messages.error(request, f"Impossible de supprimer la catégorie '{categorie.nom}' car elle contient des livres")
        return redirect('liste_categories')
    
    if request.method == 'POST':
        nom = categorie.nom
        categorie.delete()
        messages.success(request, f'Catégorie "{nom}" supprimée avec succès')
        return redirect('liste_categories')
    
    return render(request, 'categories/supprimer.html', {'categorie': categorie})

@login_required
def liste_emprunts(request):
    """Liste des emprunts - admin voit tout, client voit ses emprunts"""
    today = date.today()
    
    if request.user.role == 'admin':
        emprunts = Emprunt.objects.filter(date_retour_reelle__isnull=True).select_related('livre', 'utilisateur')
    else:
        emprunts = Emprunt.objects.filter(utilisateur=request.user, date_retour_reelle__isnull=True).select_related('livre')
    
    en_retard_count = emprunts.filter(date_retour_prevue__lt=today).count()
    
    return render(request, 'emprunts/liste.html', {
        'emprunts': emprunts,
        'en_retard_count': en_retard_count,
        'today': today
    })

@login_required
def retourner_livre(request, pk):
    """Retourner un livre - admin ou propriétaire"""
    emprunt = get_object_or_404(Emprunt, id=pk)
    
    if emprunt.utilisateur != request.user and request.user.role != 'admin':
        messages.error(request, "Vous ne pouvez retourner que vos propres emprunts")
        return redirect('liste_emprunts')
    
    if emprunt.date_retour_reelle:
        messages.error(request, "Ce livre a déjà été retourné")
        return redirect('liste_emprunts')
    
    emprunt.date_retour_reelle = date.today()
    emprunt.save()
    
    livre = emprunt.livre
    livre.quantite_disponible += 1
    livre.save()
    
    messages.success(request, f'✓ Retour du livre "{livre.titre}" enregistré')
    return redirect('liste_emprunts')

@login_required
@admin_required
def statistiques(request):
    """Statistiques - admin uniquement"""
    total_livres = Livre.objects.count()
    livres_disponibles = Livre.objects.filter(quantite_disponible__gt=0).count()
    emprunts_actifs = Emprunt.objects.filter(date_retour_reelle__isnull=True).count()
    taux = (livres_disponibles / total_livres * 100) if total_livres > 0 else 0
    
    # Calcul des pourcentages pour les catégories
    livres_par_categorie = []
    for cat in Categorie.objects.annotate(nb=Count('livres')):
        pourcentage = int((cat.nb / total_livres * 100)) if total_livres > 0 else 0
        livres_par_categorie.append({
            'nom': cat.nom,
            'count': cat.nb,
            'pourcentage': pourcentage
        })
    
    # Calcul des pourcentages pour les auteurs
    top_auteurs = []
    for auteur in Livre.objects.values('auteur').annotate(total=Count('id_livre')).order_by('-total')[:5]:
        pourcentage = int((auteur['total'] / total_livres * 100)) if total_livres > 0 else 0
        top_auteurs.append({
            'auteur': auteur['auteur'],
            'total': auteur['total'],
            'pourcentage': pourcentage
        })
    
    context = {
        'total_livres': total_livres,
        'livres_disponibles': livres_disponibles,
        'taux_disponibilite': round(taux),
        'emprunts_actifs': emprunts_actifs,
        'livres_par_categorie': livres_par_categorie,
        'top_auteurs': top_auteurs,
    }
    return render(request, 'statistiques/index.html', context)

@csrf_exempt
def chatbot_question(request):
    """Chatbot - accessible à tous"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            service = ChatbotService()
            reponse = service.traiter_question(question)
            return JsonResponse({'reponse': reponse})
        except Exception as e:
            return JsonResponse({'reponse': f"❌ Erreur: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)