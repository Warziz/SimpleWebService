"""Module pour la gestion du stock et du panier dans la base de données."""

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .models import Shop, Basket, BasketMeta
from .manage_db import db


def stock(product_id, product_amount):
    """
    Ajoute ou met à jour la quantité d'un produit en stock.

    Args:
        product_id (int): L'identifiant du produit.
        product_amount (int): La quantité à ajouter.

    Returns:
        dict: Résultat de l'opération.
    """
    try:
        stmt = select(Shop).where(Shop.id == product_id).with_for_update()
        result = db.session.execute(stmt)
        product = result.scalar_one_or_none()

        if product is None:
            new_product = Shop(id=product_id, product_amount=product_amount)
            db.session.add(new_product)
        else:
            product.product_amount += product_amount

        db.session.commit()
        return {"result": "ok"}

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"result": "error", "message": str(e)}


def update_basket(basket_id, items):
    """
    Met à jour le panier avec les produits sélectionnés, après vérification du stock.

    Args:
        basket_id (int): Identifiant du panier.
        items (list): Liste de dictionnaires contenant les produits et quantités.

    Returns:
        dict: Résultat de l'opération.
    """
    for item in items:
        product = db.session.get(Shop, item["id"])
        if not product or product.product_amount < item["amount"]:
            return {"result": "oos"}

    if not db.session.get(BasketMeta, basket_id):
        db.session.add(BasketMeta(id=basket_id))
        db.session.flush()  # S'assure que l'ID est dispo pour les FK

    # Supprime les anciens items du panier
    Basket.query.filter_by(basket_id=basket_id).delete()

    for item in items:
        new_item = Basket(
            basket_id=basket_id,
            product_id=item["id"],
            amount=item["amount"]
        )
        db.session.add(new_item)

    db.session.commit()
    return {"result": "ok"}

def checkout_basket(basket_id):
    """
    Valide le panier et décrémente les quantités de produits.

    Args:
        basket_id (int): Identifiant du panier à valider.

    Returns:
        list: Liste des produits retirés du stock.
    """
    basket = db.session.get(BasketMeta, basket_id)
    if not basket:
        return {"result": [], "message": "No basket ID known"}

    items = Basket.query.filter_by(basket_id=basket_id).all()
    if not items:
        return {"result":[]}

    for item in items:
        product = db.session.get(Shop, item.product_id)
        if product:
            product.product_amount -= item.amount
        db.session.delete(item)
    db.session.commit()
    return [{"id": item.product_id, "amount": item.amount} for item in items]



def fetch_stock():
    """
    Récupère tous les produits encore en stock.

    Returns:
        list: Liste des produits disponibles.
    """
    available_products = Shop.query.filter(Shop.product_amount > 0).all()
    return [{"id": item.id, "amount": item.product_amount} for item in available_products]
