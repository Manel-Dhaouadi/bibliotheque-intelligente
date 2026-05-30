import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-key-for-dev')

# ⚠️ IMPORTANT: DEBUG = False en production
DEBUG = False

# ⚠️ IMPORTANT: Ajouter ton URL PythonAnywhere
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    'tonusername.pythonanywhere.com',  # ← Remplace par ton username
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comptes',
    'livres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← AJOUTER pour fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'bibliotheque.middleware.ForceReauthMiddleware',  # ← Désactiver si fichier manquant
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

# ⚠️ IMPORTANT: Changer pour MySQL sur PythonAnywhere (pas PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tonusername$bibliotheque_db',  # ← $ est obligatoire
        'USER': 'tonusername',  # ← Ton username PythonAnywhere
        'PASSWORD': os.getenv('DB_PASSWORD', 'ton_mot_de_passe'),
        'HOST': 'tonusername.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
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

# ⚠️ IMPORTANT: Configuration des fichiers statiques
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

# ✅ Session corrigée
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # ← False pour rester connecté
SESSION_COOKIE_AGE = 604800  # ← 7 jours (pas 3060)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False  # ← False sur PythonAnywhere (pas de HTTPS gratuit)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'