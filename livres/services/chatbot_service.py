from ..models import Livre, Categorie, ConversationChatbot
from .gemini_service import GeminiService

class ChatbotService:
    """Chatbot avec mémoire Gemini et historique"""
    
    def __init__(self, utilisateur=None):
        self.utilisateur = utilisateur
        self.gemini = GeminiService()
    
    def _construire_prompt(self, question, historique=[], message_count=0):
        """Construire le prompt à envoyer à Gemini avec l'historique"""
        
        # Récupérer tous les livres pour le contexte (limité à 15 pour la vitesse)
        livres = Livre.objects.select_related('categorie').all()[:15]
        
        if not livres.exists():
            contexte_livres = "Aucun livre dans la bibliothèque."
        else:
            contexte_livres = "Catalogue:\n"
            for livre in livres:
                cat = livre.categorie.nom if livre.categorie else "Sans catégorie"
                contexte_livres += f"- {livre.titre} ({livre.auteur}) [{livre.quantite_disponible}/{livre.quantite_totale}]\n"
        
        # Vérifier si c'est le premier message
        is_first = (message_count <= 1 and len(historique) == 0)
        
        # Construire l'historique rapidement
        historique_texte = ""
        if historique and len(historique) > 0:
            historique_texte = "Conversation récente:\n"
            for h in historique[-4:]:  # Limité à 4 pour la vitesse
                historique_texte += f"User: {h.get('question', '')}\nBot: {h.get('reponse', '')[:100]}\n"
        
        # Prompt court et efficace
        if is_first:
            return f"""Tu es un assistant de bibliothèque sympa. Sois naturel et concis.

{contexte_livres}

{historique_texte}

Question: {question}

Règles: Réponds en français avec des émojis. Sois utile sans être trop long.

Réponse:"""
        else:
            return f"""Continue la conversation. INTERDICTION TOTALE de dire Bonjour ou toute salutation.

{contexte_livres}

{historique_texte}

Question: {question}

RÈGLE: Réponds DIRECTEMENT sans Bonjour. Sois naturel. Utilise des émojis.

Réponse:"""
    
    def traiter_question(self, question, historique=[], message_count=0):
        """Traiter la question avec l'historique"""
        prompt = self._construire_prompt(question, historique, message_count)
        reponse = self.gemini.generer_reponse(prompt)
        
        # Nettoyer les salutations si encore présentes (sauf premier message)
        if reponse and message_count > 1:
            salutations = ["Bonjour", "Bonsoir", "Salut", "Hello", "Bonjour !", "Salut !"]
            for sal in salutations:
                if reponse.strip().startswith(sal):
                    reponse = reponse.strip()[len(sal):].lstrip(" !,.:;")
                    break
        
        if reponse is None:
            reponse = "📚 Service IA indisponible. Réessaie dans quelques instants."
        
        # Sauvegarder
        if self.utilisateur and self.utilisateur.is_authenticated:
            ConversationChatbot.objects.create(
                utilisateur=self.utilisateur,
                question=question,
                reponse=reponse
            )
        
        return reponse
    
    def get_historique_utilisateur(self, limit=20):
        """Récupérer l'historique des conversations"""
        if not self.utilisateur or not self.utilisateur.is_authenticated:
            return []
        
        conversations = ConversationChatbot.objects.filter(
            utilisateur=self.utilisateur
        ).order_by('date_creation')[:limit]
        
        historique = []
        for conv in conversations:
            historique.append({
                'question': conv.question,
                'reponse': conv.reponse,
                'date': conv.date_creation.strftime('%d/%m/%Y %H:%M')
            })
        
        return historique