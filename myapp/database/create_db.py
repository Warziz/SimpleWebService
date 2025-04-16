"""Création des tables de la base de données à partir des modèles déclarés."""
import logging
from .manage_db import db


def create(app):
    """
    Crée les tables de la base de données en utilisant les modèles définis.

    Args:
        app: L'application Flask utilisée pour établir le contexte de l'application.
    """
    with app.app_context():
        db.create_all()
        logging.info("Tables créées ou déjà existantes.")
