from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Décorateur qui vérifie si l'utilisateur est connecté
    Si non connecté, redirige vers la page de connexion
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si l'identifiant utilisateur est dans la session
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page', 'warning')
            return redirect(url_for('auth.login'))
        # Si l'utilisateur est connecté, continue l'exécution de la fonction
        return f(*args, **kwargs)
    return decorated_function
