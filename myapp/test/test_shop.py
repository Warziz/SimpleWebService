# test_api.py

import os
import pytest
from myapp import create_app
from myapp.database.manage_db import db
from myapp.error.error_handler import register_error_handlers
from myapp.route import init_routes

@pytest.fixture
def app():
    app = create_app(config_name=os.getenv("CONFIG_TYPE"))
    app.testing = True 
    register_error_handlers(app)
    db.init_app(app)
    init_routes(app)
    return app

@pytest.fixture
def init_db(app):
    # Crée les tables dans la base de données en mémoire
    with app.app_context():
        db.create_all()
        print("Tables créées :", db.metadata.tables.keys())
        yield db
        # Nettoie la base de données après chaque test
        db.session.remove()
        db.drop_all()

#Ajoute en plusieurs fois 1 item dans la BDD
def test_add_multiple_item(app,init_db):

    data = [{"id": 123, "amount": 1}]

    for i in range (10):
        client =app.test_client()
        response = client.put('/shop/stock',json=data)

        assert response.status_code == 200
        assert "result" in response.json
        assert response.json["result"] == "ok"

#Ajoute plusieurs items en une fois
def test_add_items(app):
    
    data = [{"id": 123, "amount": 1},{"id": 13, "amount": 34},{"id": 12, "amount": 356}]
    client =app.test_client()
    response = client.put('/shop/stock',json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "ok"



#Ajoute plusieurs items en une fois
def test_add_to_basket(app,init_db):
    
    data = [{"id": 101, "amount": 10},{"id": 102, "amount": 34},{"id": 12, "amount": 356}]
    
    client =app.test_client()
    response = client.put('/shop/stock',json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "ok"
    
    data = {
        'id': 1,
        'basket': [
            {'id': 101, 'amount': 2},
            {'id': 102, 'amount': 1}
        ]
    }

    client = app.test_client()
    response = client.post('/shop/basket', json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "ok"

#Prend trop dans les stock
def test_take_to_much(app,init_db):
    
    data = [{"id": 101, "amount": 10},{"id": 102, "amount": 34},{"id": 12, "amount": 356}]
    
    client =app.test_client()
    response = client.put('/shop/stock',json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "ok"
    
    data = {
        'id': 1,
        'basket': [
            {'id': 101, 'amount': 12}
        ]
    }

    client = app.test_client()
    response = client.post('/shop/basket', json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "oos"

#Prendre un panier qui n'existe pas
def test_checkout_no_basket(app,init_db):
    
    data = {
        'id': 1897,
        'basket': [
            {'id': 101, 'amount': 2},
            {'id': 102, 'amount': 1}
        ]
    }

    client = app.test_client()
    response = client.post('/shop/checkout', json=data)
    assert response.status_code == 200
    assert response.json["result"] == "error"
    assert response.json["message"] == "Invalid basket ID"

#Créer un panier vide et le checkout
def test_checkout_empty_basket(app,init_db):
    
    data = {
        'id': 1897,
        'basket': []
    }

    client = app.test_client()
    response = client.post('/shop/basket', json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "ok"

    response = client.post('/shop/checkout',json=data)
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == []


