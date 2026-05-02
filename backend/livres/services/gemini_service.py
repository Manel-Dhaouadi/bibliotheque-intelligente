import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """Service pour interagir avec l'API Google Gemini"""
    
    def __init__(self):
        """Initialiser le service Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY non trouvée dans les variables d'environnement")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generer_reponse(self, prompt, contexte):
        """Générer une réponse intelligente basée sur le contexte"""
        try:
            # Construction du prompt complet avec contexte
            prompt_complet = f"""
            Tu es un assistant bibliothécaire expert. Voici le contexte de la bibliothèque :
            {contexte}
            
            Question de l'utilisateur : {prompt}
            
            Règles à suivre :
            1. Réponds uniquement en français
            2. Sois précis et utilitaire
            3. Si tu ne connais pas la réponse, dis-le honnêtement
            4. Utilise les informations du contexte fourni
            5. Sois courtois et professionnel
            
            Réponse :
            """
            
            response = self.model.generate_content(prompt_complet)
            return response.text
        
        except Exception as e:
            return f"Désolé, une erreur s'est produite : {str(e)}"