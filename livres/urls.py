from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livres/ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('livres/<int:pk>/modifier/', views.modifier_livre, name='modifier_livre'),
    path('livres/<int:pk>/supprimer/', views.supprimer_livre, name='supprimer_livre'),
    path('livres/<int:pk>/emprunter/', views.emprunter_livre, name='emprunter_livre'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/<int:pk>/modifier/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/<int:pk>/supprimer/', views.supprimer_categorie, name='supprimer_categorie'),
    path('emprunts/', views.liste_emprunts, name='liste_emprunts'),
    path('emprunts/<int:pk>/retourner/', views.retourner_livre, name='retourner_livre'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('api/chatbot/question/', views.chatbot_question, name='chatbot_question'),
    path('api/chatbot/historique/', views.get_chatbot_historique, name='chatbot_historique'),
]