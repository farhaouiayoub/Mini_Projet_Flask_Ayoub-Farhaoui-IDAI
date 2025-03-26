from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Modèle pour les utilisateurs dans la base de données"""
    __tablename__ = 'users'
    
    # Définition des colonnes de la table
    id = db.Column(db.Integer, primary_key=True)  # Clé primaire
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email unique
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nom d'utilisateur unique
    password_hash = db.Column(db.String(128), nullable=False)  # Mot de passe hashé pour la sécurité
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création du compte
    last_login = db.Column(db.DateTime, nullable=True)  # Date de dernière connexion
    
    def __init__(self, email, username, password):
        """Constructeur pour initialiser un nouvel utilisateur"""
        self.email = email
        self.username = username
        self.set_password(password)  # Hash du mot de passe
    
    def set_password(self, password):
        """Méthode pour hasher le mot de passe"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Méthode pour vérifier si le mot de passe est correct"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Méthode pour mettre à jour la date de dernière connexion"""
        self.last_login = datetime.utcnow()
        db.session.commit()
        
    def to_dict(self):
        """Convertit l'objet utilisateur en dictionnaire pour le cache et les API"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
        
    @classmethod
    def find_by_email(cls, email):
        """Méthode de classe pour trouver un utilisateur par son email"""
        return cls.query.filter_by(email=email).first()
