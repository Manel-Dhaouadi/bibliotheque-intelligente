from django.contrib import admin
from .models import Categorie, Livre, Emprunt

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_livres']
    search_fields = ['nom']

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'quantite_disponible', 'statut']
    list_filter = ['categorie', 'statut', 'annee_publication']
    search_fields = ['titre', 'auteur']
    readonly_fields = ['date_ajout', 'date_modification']

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ['livre', 'utilisateur_nom', 'date_emprunt', 'date_retour_prevue', 'est_en_retard']
    list_filter = ['date_emprunt']
    search_fields = ['utilisateur_nom']