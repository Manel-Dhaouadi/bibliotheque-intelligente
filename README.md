# 📚 Bibliothèque Intelligente avec Chatbot IA

## 🎯 Objectif du projet
Application web complète de gestion de bibliothèque avec :
- Gestion des livres (CRUD complet)
- Chatbot intelligent utilisant Google Gemini AI
- Interface moderne avec React.js
- API REST avec Django

## 🛠 Technologies utilisées

### Backend
- Django 5.0
- Django REST Framework
- PostgreSQL
- Google Gemini AI
- Python-dotenv

### Frontend
- React 18
- Vite
- Axios
- React Router DOM

## 📁 Structure du projet
bibliotheque_intelligente/
├── backend/ # API Django
├── frontend/ # Application React
├── .gitignore
└── README.md

## 🚀 Installation

### Prérequis
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver