"""Endpoints de l'API liés à la gestion du stock, des paniers, et des commandes."""

from flask import Blueprint, request, jsonify
from ..database import stock, update_basket, checkout_basket, fetch_stock

shop_api = Blueprint('shop_api', __name__)


def is_valid_uint32(value):
    """Vérifie si une valeur est un entier non signé 32 bits (0 à 4 294 967 295)."""
    return isinstance(value, int) and 0 <= value <= 4294967295


@shop_api.route('/shop/stock', methods=["PUT"])
def add_stock():
    """Ajoute des produits au stock avec vérification des IDs."""
    data = request.get_json(force=True)

    for item in data:
        product_id = item.get("id")
        product_amount = item.get("amount")

        if not is_valid_uint32(product_id) or not isinstance(product_amount, int) or product_amount < 0:
            return jsonify({"result": "error", "message": "Invalid product ID or amount"}), 400

        stock(product_id, product_amount)

    return jsonify({"result": "ok"})


@shop_api.route("/shop/basket", methods=["POST"])
def modify_basket():
    """Modifie un panier après validation des identifiants."""
    data = request.get_json(force=True)

    if "id" not in data or "basket" not in data:
        return jsonify({"result": "error", "message": "Invalid request"}), 400

    basket_id = data["id"]
    if not is_valid_uint32(basket_id):
        return jsonify({"result": "error", "message": "Invalid basket ID"}), 400

    items = data["basket"]
    for item in items:
        if "id" not in item or "amount" not in item:
            return jsonify({"result": "error", "message": "Invalid basket format"}), 400

        if not is_valid_uint32(item["id"]) or not isinstance(item["amount"], int) or item["amount"] < 0:
            return jsonify({"result": "error", "message": "Invalid product ID or amount"}), 400

    result = update_basket(basket_id, items)
    return jsonify(result)


@shop_api.route("/shop/checkout", methods=["POST"])
def checkout():
    """Confirme une commande après vérification de l'ID du panier."""
    data = request.get_json(force=True)

    if "id" not in data:
        return jsonify({"result": "error", "message": "Missing basket ID"}), 400

    basket_id = data["id"]
    if not is_valid_uint32(basket_id):
        return jsonify({"result": "error", "message": "Invalid basket ID"}), 400

    order = checkout_basket(basket_id)
    return jsonify(order)


@shop_api.route("/shop/stock", methods=["GET"])
def get_stock():
    """Récupère l'état du stock."""
    stock_data = fetch_stock()
    return jsonify(stock_data if stock_data else []), 200
