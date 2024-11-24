from flask import Blueprint, render_template, session, redirect, url_for
from . import token_required, get_secret_key
import jwt

from .models import Usuario

views = Blueprint("views", __name__)


def get_email():
    user = session.get("profile")

    if user:
        return user["email"]

    token = session.get("token")
    dados = jwt.decode(token, get_secret_key(), algorithms="HS256")
    return dados["email"]


def check_adm(email):
    usuario = Usuario.query.filter_by(email=email).first()
    return usuario and usuario.role and usuario.role.name == "admin"


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/auth")
@token_required
def auth():
    email = get_email()
    adm = check_adm(email=email)

    return render_template("dashUsuarios.html", email=email, adm=adm)


@views.route("/denied")
def denied():
    return render_template("acessoNegado.html")


@views.route("/adm")
@token_required
def adm():
    email = get_email()
    adm = check_adm(email=email)

    if adm:
        return render_template("adm.html")
    else:
        return redirect(url_for("views.denied"))
