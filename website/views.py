from flask import Blueprint, render_template
from . import token_required

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/auth")
@token_required
def auth():
    return render_template("dashUsuarios.html")


@views.route("/denied")
def denied():
    return render_template("acessoNegado.html")
