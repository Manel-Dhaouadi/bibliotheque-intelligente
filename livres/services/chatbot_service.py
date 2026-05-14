from ..models import Livre, Categorie
from .gemini_service import GeminiService

class ChatbotService:
    """Chatbot 100% IA avec Gemini - Pas de logique conditionnelle"""
    
    def __init__(self):
        self.gemini = GeminiService()
    
    def _construire_prompt(self, question):
        """Construire le prompt à envoyer à Gemini"""
        
        # Récupérer tous les livres pour le contexte
        livres = Livre.objects.select_related('categorie').all()
        
        if not livres.exists():
            contexte_livres = "Aucun livre dans la bibliothèque pour le moment."
        else:
            contexte_livres = "Voici le catalogue complet :\n"
            for livre in livres:
                cat = livre.categorie.nom if livre.categorie else "Non catégorisé"
                contexte_livres += f"- {livre.titre} | {livre.auteur} | {cat} | {livre.quantite_disponible}/{livre.quantite_totale} ex.\n"
        
        return f"""
Tu es un assistant bibliothécaire. Voici le catalogue :
{contexte_livres}

Question: "{question}"

Instructions:
- Réponds en français avec des émojis
- Sois naturel et conversationnel
- Utilise UNIQUEMENT les livres du catalogue
- Si la question concerne un livre qui n'existe pas, dis-le poliment et propose des alternatives du catalogue
- Réponds même aux questions personnelles (comment tu vas, ton nom, etc.)

Réponse:"""
    
    def traiter_question(self, question):
        """Traiter la question exclusivement avec Gemini"""
        prompt = self._construire_prompt(question)
        reponse = self.gemini.generer_reponse(prompt)
        
        # Si Gemini échoue (API down), retourner un message simple
        if reponse is None:
            return "📚 Service IA momentanément indisponible. Veuillez réessayer dans quelques instants."
        
        return reponse