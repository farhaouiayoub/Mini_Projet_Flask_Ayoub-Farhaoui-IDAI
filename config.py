import os
from datetime import timedelta

class Config:
    """Classe de configuration pour l'application Flask"""
    
    # Clé secrète pour la sécurité (signatures des cookies, tokens)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive les signaux de modifications
    
    # Configuration des sessions et du cache
    SESSION_TYPE = 'filesystem'  # Stocke les sessions dans des fichiers
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Durée de vie des sessions
    CACHE_TYPE = 'simple'  # Type de cache simple (en mémoire)
    CACHE_DEFAULT_TIMEOUT = 300  # Durée de vie par défaut des entrées de cache (5 minutes)
