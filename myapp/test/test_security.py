#test_security.py

import os
import pytest
from myapp import create_app
from myapp.database.manage_db import db
from myapp.error.error_handler import register_error_handlers
from myapp.route import init_routes

@pytest.fixture
def app():
    app = create_app(config_name=os.getenv("CONFIG_TYPE"))
    
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

#Vérifie une injection SQL
def test_sql_injection(app,init_db):

    data = {
        'user': "admin",
        'secret': 'any_password'
    }

    client = app.test_client()
    response = client.post('/totp/auth', json=data, headers={"X-User": "' OR '1'='1 --"})
    assert response.status_code == 400
    assert "result" in response.json
    assert response.json["result"] == "error"

def test_sql_injection_username(app, init_db):
    client = app.test_client()
    malicious_user = "'; DROP TABLE users; --"
    response = client.put('/totp/register', json={"user": malicious_user, "secret": "AAAA"})
    assert response.status_code == 400
    print("Tables créées :", db.metadata.tables.keys())

#Vérifie que le header user est bien présent
def test_auth_without_user_header(app, init_db):
    client = app.test_client()
    response = client.post('/totp/auth', json={"password": "dummy"})
    assert response.status_code == 400 or response.status_code == 401

#Envoie un json invalide
def test_invalid_json_payload(app,init_db):
    client = app.test_client()
    response = client.put('/totp/register', data="not a json", content_type='application/json')
    assert response.status_code == 500