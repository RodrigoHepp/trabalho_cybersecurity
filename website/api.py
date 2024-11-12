from flask import Blueprint, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from . import db
from .models import Usuario

api = Blueprint("api", __name__)


@api.route("/login", methods=["POST"])
def login():
    if request.method != "POST":
        return redirect(url_for("auth.login"))

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

    print("Usuario Logado Com Sucesso")
    return redirect(url_for("views.home"))


@api.route("/logout")
def logout():
    # TODO: LIMPAR OS TOKENS

    return redirect(url_for("views.home"))


@api.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method != "POST":
        return redirect(url_for("auth.sign_up"))

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
