from flask_caching import Cache

# Création de l'instance de cache
cache = Cache()

def init_cache(app):
    """
    Initialise le système de cache pour l'application
    Le cache est utilisé pour stocker temporairement des données fréquemment utilisées
    et éviter des requêtes répétées à la base de données
    """
    cache.init_app(app)
    return cache
