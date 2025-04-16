"""Définit la route pour le service de calculatrice."""

from flask import Blueprint, request
from ..modules import calculatrice

calc = Blueprint('calc', __name__)

@calc.route('/calculatrice', methods=["GET"])
def get_calcul():
    """Évalue une expression mathématique passée en paramètre GET."""
    expr = request.args.get('expr')
    return str(calculatrice(expr))
