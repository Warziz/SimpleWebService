"""Gère l'enregistrement et l'authentification des utilisateurs via TOTP."""

from flask import Blueprint, request, jsonify
from ..database import register_user, get_auth

authenticate = Blueprint('authenticate', __name__)

@authenticate.route('/totp/register', methods=["PUT"])
def sign_user():
    """Inscrit un utilisateur avec son secret TOTP."""
    data = request.get_json(force=True)
    if not data or "secret" not in data or "user" not in data:
        return jsonify({"result": "error", "message": "Invalid request"}), 400

    user = data.get("user")
    secret = data.get("secret")

    message = register_user(user, secret)

    if "Erreur" in message:
        return jsonify({"result": "error", "message": message}), 400

    return jsonify({"result": "ok"})


@authenticate.route('/totp/auth', methods=['POST'])
def auth():
    """Vérifie l'authentification d'un utilisateur via TOTP."""
    user = request.headers.get("X-User")
    data = request.get_json(force=True)

    if not user or not data or "password" not in data:
        return jsonify({"result": "error", "message": "Invalid request"}), 400

    secret = data.get("password")
    result = get_auth(user, secret)

    if result == "unauthorized":
        return jsonify({"result": "unauthorized"}), 401

    return jsonify({"result": "ok"})