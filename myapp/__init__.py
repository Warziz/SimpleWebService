"""Module d'initialisation de l'application Flask."""

import os
from flask import Flask
from myapp.route import init_routes
from myapp.database.create_db import create
from myapp.database.manage_db import init_db
from myapp.error.error_handler import register_error_handlers
from dotenv import load_dotenv

def create_app(config_name) -> Flask:
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    print(config_name)
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        register_error_handlers(app)
        init_db(app)
        create(app)
        init_routes(app)
    return app

load_dotenv()

app = create_app(config_name=os.getenv("CONFIG_TYPE"))