"""Gestion de l'enregistrement des utilisateurs et de leur authentification."""

import hashlib
from datetime import datetime, timezone

from .models import User
from .manage_db import db
from ..wrapper.ciphering import encrypt_secret, decrypt_secret


def register_user(username, secret):
    """
    Enregistre un nouvel utilisateur après vérification des contraintes de longueur.
    Chiffre le secret avant de l'enregistrer.

    Args:
        username (str): Nom d'utilisateur à enregistrer.
        secret (str): Secret à chiffrer et sauvegarder.

    Returns:
        str: Message de succès ou d'erreur.
    """
    if len(username) < 4:
        return ValueError("Username too short")
    if len(username) > 16:
        raise ValueError("Username too long")
    if len(secret) < 8:
        raise ValueError("Secret too short")
    if len(secret) > 64:
        raise ValueError("Secret too long")

    if User.query.filter_by(username=username).first():
        return f"Erreur : L'utilisateur '{username}' existe déjà."

    cipher = encrypt_secret(secret)
    new_user = User(username=username, secret=cipher)
    db.session.add(new_user)
    db.session.commit()
    return f"Utilisateur {username} enregistré avec succès."


def get_auth(username, secret):
    """
    Vérifie les informations d'identification d'un utilisateur via un hash temporel.

    Args:
        username (str): Nom d'utilisateur fourni.
        secret (str): Hash SHA-256 attendu (trunc à 16 chars).

    Returns:
        str: "ok" si authentifié, sinon "unauthorized"
    """
    utc_now = datetime.now(timezone.utc)
    time_str = utc_now.strftime("%Y%m%d-%H%M")

    user = User.query.filter_by(username=username).first()
    if not user:
        return "unauthorized"

    passwd = decrypt_secret(user.secret)
    concat = (passwd + time_str).encode()
    expected = hashlib.sha256(concat).hexdigest()[:16]

    return "ok" if expected == secret else "unauthorized"
