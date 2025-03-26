from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController
from utils.decorators import login_required

# Création d'un Blueprint pour regrouper les routes liées à l'authentification
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Route pour l'inscription d'un nouvel utilisateur"""
    # Si l'utilisateur est déjà connecté, redirige vers le profil
    if 'user_id' in session:
        return redirect(url_for('auth.profile'))
        
    # Traitement du formulaire d'inscription
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Appel du contrôleur pour créer l'utilisateur
        success, message = AuthController.register_user(
            email, username, password, confirm_password
        )
        
        # Affichage d'un message flash pour informer l'utilisateur
        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('auth.login'))  # Redirection vers la page de connexion
    
    # Affichage du formulaire d'inscription
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Route pour la connexion d'un utilisateur"""
    # Si l'utilisateur est déjà connecté, redirige vers le profil
    if 'user_id' in session:
        return redirect(url_for('auth.profile'))
        
    # Traitement du formulaire de connexion
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False  # Option "se souvenir de moi"
        
        # Appel du contrôleur pour vérifier les identifiants
        success, message = AuthController.login_user(email, password, remember)
        
        # Affichage d'un message flash
        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('auth.profile'))  # Redirection vers le profil
    
    # Affichage du formulaire de connexion
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Route pour la déconnexion"""
    AuthController.logout_user()
    flash('Vous avez été déconnecté avec succès', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required  # Décorateur pour vérifier que l'utilisateur est connecté
def profile():
    """Route pour afficher le profil de l'utilisateur"""
    user_data = AuthController.get_current_user()  # Récupération des données de l'utilisateur
    return render_template('profile.html', user=user_data)

@auth_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required  # Décorateur pour vérifier que l'utilisateur est connecté
def edit_profile():
    """Route pour modifier le profil de l'utilisateur"""
    # Récupération des données actuelles de l'utilisateur
    user_data = AuthController.get_current_user()
    
    # Traitement du formulaire de modification
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Appel du contrôleur pour mettre à jour les informations
        success, message = AuthController.update_user(
            username, email, current_password, new_password, confirm_password
        )
        
        # Affichage d'un message flash
        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('auth.profile'))  # Redirection vers le profil
    
    # Affichage du formulaire de modification
    return render_template('edit_profile.html', user=user_data)
