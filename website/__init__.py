from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SENHA_DB = os.getenv("SENHA_DB")
NOME_BANCO = os.getenv("NOME_BANCO")
URL_BANCO = f"mysql+pymysql://root:{SENHA_DB}@localhost/{NOME_BANCO}"

db = SQLAlchemy()


def cria_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = URL_BANCO
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api")

    # cria_database(app)

    return app


def cria_database(app):
    with app.app_context():
        db.create_all()
