from ..models import Livre, Categorie, Emprunt
from django.db.models import Q
from datetime import date
from .gemini_service import GeminiService
import re

class ChatbotService:
    """Service intelligent pour le chatbot de la bibliothèque"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
    
    def get_contexte_bibliotheque(self):
        """Récupérer le contexte complet de la bibliothèque"""
        livres_total = Livre.objects.count()
        livres_disponibles = Livre.objects.filter(quantite_disponible__gt=0).count()
        categories = Categorie.objects.all()
        
        contexte = f"""
        STATISTIQUES DE LA BIBLIOTHÈQUE:
        - Nombre total de livres: {livres_total}
        - Livres actuellement disponibles: {livres_disponibles}
        
        CATÉGORIES ET LIVRES:
        """
        
        for categorie in categories:
            livres_cat = Livre.objects.filter(categorie=categorie)
            contexte += f"\n{categorie.nom}: {livres_cat.count()} livres"
            for livre in livres_cat[:5]:  # Limite à 5 livres par catégorie
                statut = "Disponible" if livre.est_disponible else "Non disponible"
                contexte += f"\n  - {livre.titre} par {livre.auteur} ({livre.annee_publication}) - {statut} ({livre.quantite_disponible}/{livre.quantite_totale} exemplaires)"
        
        return contexte
    
    def rechercher_livres(self, requete):
        """Rechercher des livres dans la base de données"""
        mots_cles = requete.lower().split()
        
        # Construction de la requête de recherche
        query = Q()
        for mot in mots_cles:
            query |= Q(titre__icontains=mot)
            query |= Q(auteur__icontains=mot)
        
        livres = Livre.objects.filter(query)
        return livres
    
    def traiter_question(self, question_utilisateur):
        """Traiter la question de l'utilisateur"""
        
        # Vérifier si c'est une question sur les livres disponibles
        if any(mot in question_utilisateur.lower() for mot in ['disponible', 'existe', 'as-tu', 'avez-vous']):
            livres_trouves = self.rechercher_livres(question_utilisateur)
            
            if livres_trouves.exists():
                reponse = "📚 Voici ce que j'ai trouvé :\n\n"
                for livre in livres_trouves[:5]:
                    statut_emoji = "✅" if livre.est_disponible else "❌"
                    reponse += f"{statut_emoji} **{livre.titre}** - {livre.auteur}\n"
                    reponse += f"   📅 {livre.annee_publication} | 📖 {livre.categorie.nom if livre.categorie else 'Non catégorisé'}\n"
                    reponse += f"   Disponible: {livre.quantite_disponible}/{livre.quantite_totale} exemplaires\n\n"
                return reponse
            else:
                return "🔍 Désolé, je n'ai pas trouvé de livres correspondant à votre recherche. Voulez-vous essayer d'autres mots-clés ?"
        
        # Vérifier si c'est une demande de recommandation
        elif any(mot in question_utilisateur.lower() for mot in ['recommande', 'suggère', 'conseille', 'propose']):
            # Extraire la catégorie ou le genre recherché
            categories = Categorie.objects.all()
            livres_recommandes = Livre.objects.filter(quantite_disponible__gt=0).order_by('?')[:3]
            
            reponse = "📖 **Mes recommandations pour vous :**\n\n"
            for livre in livres_recommandes:
                reponse += f"✨ **{livre.titre}** par {livre.auteur}\n"
                reponse += f"   📚 {livre.categorie.nom if livre.categorie else 'Général'}\n"
                reponse += f"   ✅ Disponible ({livre.quantite_disponible} exemplaire(s))\n\n"
            return reponse
        
        # Pour les autres questions, utiliser Gemini
        else:
            contexte = self.get_contexte_bibliotheque()
            reponse_ia = self.gemini_service.generer_reponse(question_utilisateur, contexte)
            return reponse_ia
    
    def repondre_question_specifique(self, question):
        """Réponse pour les questions très spécifiques"""
        question_lower = question.lower()
        
        # Vérifier les emprunts
        if 'emprunt' in question_lower or 'retard' in question_lower:
            emprunts_retard = Emprunt.objects.filter(date_retour_reelle__isnull=True, date_retour_prevue__lt=date.today())
            if emprunts_retard.exists():
                return f"⚠️ Il y a actuellement {emprunts_retard.count()} emprunts en retard."
            return "✅ Aucun emprunt en retard actuellement."
        
        return None