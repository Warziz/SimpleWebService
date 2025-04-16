"""Définit la route d'accueil de l'application web."""

from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index')
def index():
    """Affiche la page d'accueil."""
    return render_template("index.html")
