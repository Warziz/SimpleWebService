import pytest
import os
from myapp import create_app
from myapp.database.manage_db import db

# Fixture pour configurer l'application pour les tests
@pytest.fixture
def app():
    # Crée l'application avec la configuration 'testing' pour utiliser la base de données en mémoire
    app = create_app(config_name=os.getenv("CONFIG_TYPE"))
    
    # Associe l'application à l'instance SQLAlchemy
    db.init_app(app)
    return app

# Fixture pour initialiser la base de données en mémoire
@pytest.fixture
def init_db(app):
    # Crée les tables dans la base de données en mémoire
    with app.app_context():
        db.create_all()  
        yield db

        # Nettoie la base de données après chaque test
        db.session.remove()
        db.drop_all()

# Test pour une expression valide
def test_calculatrice_valid_expression(init_db):
    from myapp.modules.calculatrice import calculatrice
    assert calculatrice("3 + 2") == 5

# Test pour une expression invalide
def test_calculatrice_invalid_expression(init_db):
    from myapp.modules.calculatrice import calculatrice
    with pytest.raises(ValueError):
        calculatrice("3 + abc")

# Test pour une expression longue
def test_calculatrice_complexe_expression(init_db):
    from myapp.modules.calculatrice import calculatrice
    assert calculatrice("((3*3) + (3*4)) / (2*2)") == 5.25

# Test pour une expression négative
def test_calculatrice_complexe_expression(init_db):
    from myapp.modules.calculatrice import calculatrice
    assert calculatrice("((3*3) + (3*4)) / (-2*2)") == -5.25

# Test pour une division par zéro
def test_calculatrice_invalid_expression(init_db):
    from myapp.modules.calculatrice import calculatrice
    with pytest.raises(ValueError):
        calculatrice("3 / 0")