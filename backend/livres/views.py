from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from .models import Livre, Categorie, Emprunt
from .serializers import LivreSerializer, CategorieSerializer, EmpruntSerializer
from .services.chatbot_service import ChatbotService
from django.db.models import Q

class LivreViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les opérations CRUD sur les livres"""
    
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    
    def get_queryset(self):
        """Personnaliser la recherche"""
        queryset = Livre.objects.all()
        
        # Filtre par statut
        statut = self.request.query_params.get('statut', None)
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Recherche par titre ou auteur
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(titre__icontains=search) | Q(auteur__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def emprunter(self, request, pk=None):
        """Action personnalisée pour emprunter un livre"""
        livre = self.get_object()
        
        if livre.emprunter():
            emprunt = Emprunt.objects.create(
                livre=livre,
                utilisateur_nom=request.data.get('utilisateur_nom', 'Anonyme')
            )
            return Response({
                'message': f'Livre "{livre.titre}" emprunté avec succès',
                'date_retour_prevue': emprunt.date_retour_prevue
            })
        return Response(
            {'error': 'Ce livre n\'est pas disponible'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def retourner(self, request, pk=None):
        """Action personnalisée pour retourner un livre"""
        livre = self.get_object()
        
        if livre.retourner():
            return Response({'message': f'Livre "{livre.titre}" retourné avec succès'})
        return Response(
            {'error': 'Erreur lors du retour du livre'},
            status=status.HTTP_400_BAD_REQUEST
        )

class CategorieViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les catégories"""
    
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class ChatbotViewSet(viewsets.ViewSet):
    """ViewSet pour le chatbot"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chatbot_service = ChatbotService()
    
    @action(detail=False, methods=['post'])
    def question(self, request):
        """Endpoint pour poser une question au chatbot"""
        question = request.data.get('question', '')
        
        if not question:
            return Response(
                {'error': 'Veuillez poser une question'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reponse = self.chatbot_service.traiter_question(question)
        return Response({'reponse': reponse})
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """Obtenir les statistiques de la bibliothèque"""
        total_livres = Livre.objects.count()
        livres_disponibles = Livre.objects.filter(quantite_disponible__gt=0).count()
        emprunts_actifs = Emprunt.objects.filter(date_retour_reelle__isnull=True).count()
        
        return Response({
            'total_livres': total_livres,
            'livres_disponibles': livres_disponibles,
            'taux_disponibilite': (livres_disponibles / total_livres * 100) if total_livres > 0 else 0,
            'emprunts_actifs': emprunts_actifs
        })