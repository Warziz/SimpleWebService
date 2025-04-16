# test_authentification.py

import os
import pytest
import hashlib
from datetime import datetime, timezone
from myapp import create_app
from myapp.database.manage_db import db
from myapp.route import init_routes

@pytest.fixture
def app():
    app = create_app(config_name=os.getenv("CONFIG_TYPE"))
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

# Test pour l'enregistrement d'un utilisateur
def test_register_user(app, init_db):
    data = {
        'user': 'roger',
        'secret': 'AAAAAAAA'
    }
    
    # Crée un client de test explicitement
    client = app.test_client()
    response = client.put('/totp/register', json=data)
    
    # Vérifie que la réponse contient 'result'
    assert response.status_code == 200
    assert "result" in response.json
    assert response.json["result"] == "ok"

# Test pour l'authentification d'un utilisateur
def test_auth_user(app,init_db):
    # On doit d'abord enregistrer un utilisateur
    client = app.test_client()
    response = client.put('/totp/register', json={'user': 'test_client', 'secret': 'test_secret'})
    
    assert response.status_code == 200
    
    utc_now = datetime.now(timezone.utc)
    time_str = utc_now.strftime("%Y%m%d-%H%M")

    passwd = "test_secret"
    concat = (passwd + time_str).encode()
    expected = hashlib.sha256(concat).hexdigest()[:16]

    # Ensuite, on teste l'authentification
    data = {
        'password': f'{expected}'
    }
    
    response = client.post('/totp/auth', json=data, headers={"X-User": "test_client"})
    
    # Vérifie que la réponse contient 'result'
    assert response.status_code == 200
    assert response.json["result"] == "ok"

#Test quand on fournit un mauvais mot de passe
def test_wrong_passwd(app,init_db):

    client = app.test_client()    
    utc_now = datetime.now(timezone.utc)
    time_str = utc_now.strftime("%Y%m%d-%H%M")

    passwd = "test_mauvais"
    concat = (passwd + time_str).encode()
    expected = hashlib.sha256(concat).hexdigest()[:16]

    # Ensuite, on teste l'authentification
    data = {
        'password': f'{expected}'
    }
    
    response = client.post('/totp/auth', json=data, headers={"X-User": "test_client"})
    
    # Vérifie que la réponse contient 'result'
    assert response.status_code == 401 
    assert response.json["result"] == "unauthorized"

#Test la soumission d'un mauvais utilisateur
def test_wrong_user(app,init_db):

    client = app.test_client()
    utc_now = datetime.now(timezone.utc)
    time_str = utc_now.strftime("%Y%m%d-%H%M")

    passwd = "test_secret"
    concat = (passwd + time_str).encode()
    expected = hashlib.sha256(concat).hexdigest()[:16]

    # Ensuite, on teste l'authentification
    data = {
        'password': f'{expected}'
    }
    
    response = client.post('/totp/auth', json=data, headers={"X-User": "test_wrong"})
    
    # Vérifie que la réponse contient 'result'
    assert response.status_code == 401  
    assert response.json["result"] == "unauthorized"

#Vérifie la présence d'un utilisateur qui existe déjà    
def test_user_already_exist(app, init_db):
    client = app.test_client()

    data = {
        'user': 'roger',
        'secret': 'BBBBBBBBB'
    }

    # Première tentative d'enregistrement (doit réussir)
    response1 = client.put('/totp/register', json=data)
    assert response1.status_code == 200

    # Deuxième tentative avec le même utilisateur (doit échouer)
    response2 = client.put('/totp/register', json=data)
    assert response2.status_code == 400
    assert "result" in response2.json
    assert response2.json["result"] == "error"
