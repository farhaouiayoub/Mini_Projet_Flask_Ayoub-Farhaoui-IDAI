from flask import session, flash, redirect, url_for
from models.user import User, db
from utils.cache import cache

class AuthController:
    @staticmethod 
    def register_user(email, username, password, confirm_password):
        """Méthode pour enregistrer un nouvel utilisateur"""
        # Validation des données saisies
        if not email or not username or not password or not confirm_password:
            return False, "Tous les champs sont obligatoires"
            
        if password != confirm_password:
            return False, "Les mots de passe ne correspondent pas"
            
        # Vérification si l'utilisateur existe déjà
        existing_user = User.find_by_email(email)
        if existing_user:
            return False, "Cet email est déjà enregistré"
            
        # Création du nouvel utilisateur
        try:
            new_user = User(email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return True, "Inscription réussie ! Veuillez vous connecter."
        except Exception as e:
            db.session.rollback()  # Annulation des changements en cas d'erreur
            return False, f"Échec de l'inscription: {str(e)}"
    
    @staticmethod
    def login_user(email, password, remember=False):
        """Méthode pour connecter un utilisateur"""
        # Validation des données saisies
        if not email or not password:
            return False, "Email et mot de passe sont obligatoires"
            
        # Vérification de l'existence de l'utilisateur et du mot de passe
        user = User.find_by_email(email)
        if not user or not user.check_password(password):
            return False, "Email ou mot de passe invalide"
            
        # Mise à jour de la date de dernière connexion
        user.update_last_login()
        
        # Configuration de la session
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = remember  # Session permanente si "Se souvenir de moi" est coché
        
        # Mise en cache des données utilisateur pour améliorer les performances
        cache.set(f'user_{user.id}', user.to_dict(), timeout=300)
        
        return True, "Connexion réussie !"
    
    @staticmethod
    def logout_user():
        """Méthode pour déconnecter l'utilisateur"""
        # Suppression du cache
        if 'user_id' in session:
            cache.delete(f'user_{session["user_id"]}')
            
        # Nettoyage de la session
        session.clear()
        return True, "Déconnexion réussie"
    
    @staticmethod
    def get_current_user():
        """Récupère les informations de l'utilisateur actuellement connecté"""
        if 'user_id' not in session:
            return None
            
        user_id = session['user_id']
        
        # Tentative de récupération depuis le cache (plus rapide)
        cached_user = cache.get(f'user_{user_id}')
        if cached_user:
            return cached_user
            
        # Récupération depuis la base de données si pas dans le cache
        user = User.query.get(user_id)
        if user:
            user_data = user.to_dict()
            cache.set(f'user_{user_id}', user_data, timeout=300)  # Mise en cache pour 5 minutes
            return user_data
            
        return None

    @staticmethod
    def update_user(username, email, current_password, new_password=None, confirm_password=None):
        """Méthode pour mettre à jour le profil utilisateur"""
        if 'user_id' not in session:
            return False, "Vous devez être connecté pour mettre à jour votre profil"
            
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return False, "Utilisateur non trouvé"
            
        # Vérification du mot de passe actuel
        if not user.check_password(current_password):
            return False, "Le mot de passe actuel est incorrect"
        
        # Vérification que l'email n'est pas déjà utilisé par un autre utilisateur
        if email != user.email:
            existing_user = User.query.filter(User.email == email, User.id != user_id).first()
            if existing_user:
                return False, "Cet email est déjà utilisé par un autre compte"
        
        # Vérification que le nom d'utilisateur n'est pas déjà utilisé par un autre utilisateur
        if username != user.username:
            existing_user = User.query.filter(User.username == username, User.id != user_id).first()
            if existing_user:
                return False, "Ce nom d'utilisateur est déjà utilisé par un autre compte"
        
        # Mise à jour du mot de passe si fourni
        if new_password:
            if new_password != confirm_password:
                return False, "Les nouveaux mots de passe ne correspondent pas"
            user.set_password(new_password)
        
        # Mise à jour des informations utilisateur
        user.username = username
        user.email = email
        
        try:
            db.session.commit()
            
            # Mise à jour de la session
            session['username'] = username
            
            # Mise à jour du cache
            cache.delete(f'user_{user_id}')
            cache.set(f'user_{user_id}', user.to_dict(), timeout=300)
            
            return True, "Profil mis à jour avec succès !"
        except Exception as e:
            db.session.rollback()  # Annulation des changements en cas d'erreur
            return False, f"Échec de la mise à jour du profil: {str(e)}"
