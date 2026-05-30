import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque.settings')

application = get_wsgi_application()

# === MIGRATIONS AUTO - PLACÉ APRÈS application ===
try:
    from django.core.management import call_command
    from django.db import connections
    from django.apps import apps
    import sys
    
    # Attendre que les apps soient prêtes
    apps.ready  # Force l'initialisation des apps
    
    # Vérifier si les tables existent
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        result = cursor.fetchone()
        
        # Si moins de 3 tables, exécuter les migrations
        if result[0] < 3:
            call_command('migrate', interactive=False, verbosity=0)
            call_command('collectstatic', interactive=False, verbosity=0)
            print("✅ Migrations exécutées avec succès!")
except Exception as e:
    print(f"⚠️ Note: {e}")