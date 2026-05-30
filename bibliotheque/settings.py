import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-key-for-dev')

# ⚠️ IMPORTANT: DEBUG = False pour la production
DEBUG = False

# ⚠️ IMPORTANT: Autoriser Render.com
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    '.onrender.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'comptes',
    'livres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bibliotheque.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bibliotheque.wsgi.application'

# Base de données PostgreSQL avec DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

AUTH_USER_MODEL = 'comptes.Utilisateur'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Configuration fichiers statiques
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'accueil'
LOGOUT_REDIRECT_URL = 'login'

# Session
SESSION_COOKIE_AGE = 604800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ============================================
# MIGRATION AUTOMATIQUE AU DÉMARRAGE (CORRIGÉE)
# ============================================
import sys
import logging

# Désactiver les logs pendant la migration pour éviter les erreurs
logging.disable(logging.CRITICAL)

if 'migrate' not in sys.argv and 'collectstatic' not in sys.argv and 'createsuperuser' not in sys.argv:
    try:
        from django.core.management import call_command
        from django.db import connections
        from django.db.utils import OperationalError
        
        # Vérifier la connexion à la base
        try:
            with connections['default'].cursor() as cursor:
                # Vérifie si la table 'comptes_utilisateur' existe (méthode PostgreSQL compatible)
                cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'comptes_utilisateur')")
                exists = cursor.fetchone()[0]
                
                if not exists:
                    print("🔧 Création des tables de la base de données...")
                    call_command('migrate', interactive=False, verbosity=0)
                    call_command('collectstatic', interactive=False, verbosity=0)
                    print("✅ Migrations exécutées avec succès!")
                else:
                    print("✅ Base de données déjà prête.")
        except OperationalError:
            print("⚠️ Base de données non encore disponible, migrations ignorées pour l'instant.")
            
    except Exception as e:
        print(f"⚠️ Note: {e}")

# Réactiver les logs
logging.disable(logging.NOTSET)