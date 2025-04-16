"""Initialisation de la base de données avec SQLAlchemy pour l'application Flask."""

import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()


def init_db(app):
    """
    Configure l'application Flask avec les paramètres de connexion à la base de données,
    puis initialise SQLAlchemy avec cette application.
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
