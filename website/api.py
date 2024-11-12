from flask import Blueprint, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

from . import db, get_secret_key
from .models import Usuario

api = Blueprint("api", __name__)


@api.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    senha = request.form.get("password")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        # TODO: UX
        print("Email nao existe")
        return redirect(url_for("auth.login"))

    if not check_password_hash(usuario.password, senha):
        # TODO: UX
        print("Senha invalida")
        return redirect(url_for("auth.login"))

    token = jwt.encode(
        {
            "email": email,
            "expiration": str(datetime.now() + timedelta(seconds=60)),
        },
        get_secret_key(),
        algorithm="HS256",
    )

    session["token"] = token

    return redirect(url_for("views.auth"))


@api.route("/logout", methods=["POST"])
def logout():
    if request.method != "POST":
        return redirect(url_for("views.denied"))

    for key in list(session.keys()):
        session.pop(key)

    return redirect(url_for("views.home"))


@api.route("/sign-up", methods=["POST"])
def sign_up():
    if request.method != "POST":
        return redirect(url_for("views.denied"))

    email = request.form.get("email")
    nome = request.form.get("name")
    senha = request.form.get("password")

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        # TODO: UX
        print("Este usuario ja existe")
        return redirect(url_for("auth.login"))

    # TODO: UX
    # TODO: VERIFICACOES BASICAS
    # SENHA EH MAIOR Q 'X'
    # NOME TEM MAIS Q 'X' LETRAS
    # SENHA E CONF SENHA (?)

    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuario(email=email, nome=nome, password=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for("views.home"))
