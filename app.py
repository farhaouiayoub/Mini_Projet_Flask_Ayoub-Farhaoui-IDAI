from flask import Flask, redirect, url_for
from flask_session import Session
from config import Config
from models.user import db, User
from views.auth_views import auth_bp
from utils.cache import init_cache
import os

def create_app(config_class=Config):
    # Création de l'application Flask
    app = Flask(__name__)
    # Chargement de la configuration
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    db.init_app(app)  # Initialisation de la base de données
    Session(app)      # Initialisation de la gestion des sessions
    init_cache(app)   # Initialisation du système de cache
    
    # Enregistrement des blueprints (modules de l'application)
    app.register_blueprint(auth_bp, url_prefix='')
    
    # Création d'une route pour l'URL racine qui redirige vers la page de connexion
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    # Création des tables dans la base de données
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    # Point d'entrée de l'application quand on exécute ce fichier directement
    app = create_app()
    app.run(debug=True)  # Lancement du serveur en mode débug
