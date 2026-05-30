#!/bin/bash

# Exécute les migrations
python manage.py migrate --noinput

# Collecte les fichiers statiques
python manage.py collectstatic --noinput

# Lance le serveur
exec gunicorn bibliotheque.wsgi:application