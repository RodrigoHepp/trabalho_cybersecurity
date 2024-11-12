from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt

from datetime import datetime

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

    # Se for a primeira vez rodando o app execute a linha 39 antes
    # Requer um banco 'cybersecurity'
    # Depois pode comentar novamente

    # cria_database(app)

    return app


def cria_database(app):
    with app.app_context():
        db.create_all()


def get_secret_key():
    return SECRET_KEY


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = session.get("token")
        if not token:
            return redirect(url_for("views.denied"))

        try:
            dados = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            data = dados["expiration"].split(".")[0]

            expiration = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

            # TODO: UX indicando que o token expirou
            if datetime.now() > expiration:
                return redirect(url_for("auth.login"))

        except Exception as e:
            return redirect(url_for("views.denied"))
        return func(*args, **kwargs)

    return decorated
