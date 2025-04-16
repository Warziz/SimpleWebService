"""Définit les modèles SQLAlchemy pour les utilisateurs, la boutique et les paniers."""

from .manage_db import db


class User(db.Model):
    """Modèle représentant un utilisateur."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    secret = db.Column(db.LargeBinary, nullable=False)


class Shop(db.Model):
    """Modèle représentant une boutique avec des produits en stock."""

    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    product_amount = db.Column(db.Integer, nullable=False)

class BasketMeta(db.Model):
    __tablename__ = "basket_meta"
    id = db.Column(db.Integer, primary_key=True)

class Basket(db.Model):
    """Modèle représentant un panier contenant plusieurs produits."""

    __tablename__ = 'basket'
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey("basket_meta.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("shop.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('basket_id', 'product_id', name='unique_basket_product'),
    )
