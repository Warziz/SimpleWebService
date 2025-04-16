"""Initialisation des routes de l'application Flask."""

from .home import home
from .calc import calc
from .auth import authenticate
from .shop_api import shop_api

def init_routes(app):
    """Enregistre tous les Blueprints (routes) dans l'application Flask."""
    app.register_blueprint(home)
    app.register_blueprint(calc)
    app.register_blueprint(authenticate)
    app.register_blueprint(shop_api)

