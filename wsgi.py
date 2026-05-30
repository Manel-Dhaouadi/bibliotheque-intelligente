import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque.settings')

# ⚠️ AJOUTE CE CODE POUR LES MIGRATIONS AUTO (une seule fois)
try:
    from django.core.management import call_command
    from django.db import connection
    
    # Vérifie si les tables existent déjà
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        result = cursor.fetchone()
        
        # Si moins de 5 tables, on exécute les migrations
        if result[0] < 5:
            call_command('migrate', interactive=False)
            call_command('collectstatic', interactive=False)
            print("✅ Migrations exécutées avec succès!")
except Exception as e:
    print(f"⚠️ Erreur migrations: {e}")

application = get_wsgi_application()