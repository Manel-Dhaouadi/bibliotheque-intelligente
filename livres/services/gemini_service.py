import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """Service API Gemini - Détection automatique du modèle"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY non trouvée")
        
        genai.configure(api_key=self.api_key)
        
        # Détection automatique du meilleur modèle disponible
        modeles_disponibles = list(genai.list_models())
        
        # Chercher un modèle qui supporte generateContent
        modele_trouve = None
        for model in modeles_disponibles:
            if 'generateContent' in model.supported_generation_methods:
                # Prendre le premier modèle disponible
                modele_trouve = model.name
                break
        
        if not modele_trouve:
            raise ValueError("Aucun modèle disponible pour generateContent")
        
        # Nettoyer le nom du modèle (enlever 'models/')
        self.model_name = modele_trouve.replace('models/', '')
        self.model = genai.GenerativeModel(self.model_name)
        
        print(f"✅ Gemini initialisé avec: {self.model_name}")
    
    def generer_reponse(self, prompt):
        """Générer une réponse via Gemini"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else None
        except Exception as e:
            print(f"Erreur Gemini: {e}")
            return None