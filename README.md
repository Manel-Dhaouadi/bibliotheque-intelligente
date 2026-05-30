# 📚 Bibliothèque Intelligente avec Chatbot IA

## 🎯 Objectif du projet
Application web complète de gestion de bibliothèque avec :
- Gestion des livres (CRUD complet)
- Gestion des catégories
- Gestion des emprunts et retours
- Chatbot intelligent utilisant **Google Gemini AI**
- Interface responsive (mobile/desktop)
- Tableau de bord statistiques
- Authentification (Admin / Client)

## 🛠 Technologies utilisées

### Backend
- **Django 5.0** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données
- **Google Gemini AI** - Chatbot intelligent
- **Python-dotenv** - Gestion des variables d'environnement

### Frontend
- **Django Templates** - Moteur de templates
- **TailwindCSS** - Framework CSS
- **JavaScript** - Interactions dynamiques
- **FontAwesome** - Icônes

## 📁 Structure du projet

bibliotheque_intelligente/
├── bibliotheque/ # Configuration du projet Django
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── middleware.py
├── comptes/ # Application d'authentification
│ ├── models.py # Utilisateur personnalisé
│ ├── views.py
│ ├── forms.py
│ └── decorators.py
├── livres/ # Application principale
│ ├── models.py # Livre, Categorie, Emprunt
│ ├── views.py
│ ├── forms.py
│ ├── serializers.py
│ ├── permissions.py
│ └── services/
│ ├── chatbot_service.py
│ └── gemini_service.py
├── templates/ # Templates HTML
│ ├── base.html
│ ├── accueil.html
│ ├── livres/
│ ├── categories/
│ ├── emprunts/
│ └── statistiques/
├── static/ # Fichiers statiques
│ ├── css/
│ └── js/
├── staticfiles/ # Fichiers statiques collectés
├── media/ # Fichiers uploadés
├── .env # Variables d'environnement
├── requirements.txt
└── manage.py


## 🚀 Installation

### Prérequis
- Python 3.10+
- PostgreSQL 15+

### 1. Cloner le projet
```bash
git clone https://github.com/Manel-Dhaouadi/bibliotheque-intelligente.git
cd bibliotheque-intelligente