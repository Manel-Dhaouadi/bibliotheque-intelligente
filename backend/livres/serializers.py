from rest_framework import serializers
from .models import Livre, Categorie, Emprunt

class CategorieSerializer(serializers.ModelSerializer):
    nombre_livres = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description', 'nombre_livres']

class LivreSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    est_disponible = serializers.BooleanField(read_only=True)
    taux_disponibilite = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Livre
        fields = [
            'id_livre', 'titre', 'auteur', 'categorie', 'categorie_nom',
            'annee_publication', 'quantite_disponible', 'quantite_totale',
            'statut', 'est_disponible', 'taux_disponibilite',
            'date_ajout', 'date_modification'
        ]
    
    def validate(self, data):
        """Validation personnalisée"""
        if data.get('quantite_disponible', 0) > data.get('quantite_totale', 0):
            raise serializers.ValidationError(
                "La quantité disponible ne peut pas dépasser la quantité totale"
            )
        return data

class EmpruntSerializer(serializers.ModelSerializer):
    livre_titre = serializers.CharField(source='livre.titre', read_only=True)
    est_en_retard = serializers.BooleanField(read_only=True)
    jours_retard = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Emprunt
        fields = [
            'id', 'livre', 'livre_titre', 'utilisateur_nom',
            'date_emprunt', 'date_retour_prevue', 'date_retour_reelle',
            'est_en_retard', 'jours_retard'
        ]