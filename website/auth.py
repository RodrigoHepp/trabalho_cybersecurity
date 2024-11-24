from flask import Blueprint, render_template, redirect, url_for, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

from . import db, get_secret_key, oauth
from .models import Usuario

from . import token_required


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login_get():
    token = session.get("token")
    user = session.get("profile")

    if user:
        return redirect(url_for("views.auth"))

    if token:
        dados = jwt.decode(token, get_secret_key(), algorithms="HS256")
        data = dados["expiration"].split(".")[0]

        expiration = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

        if datetime.now() > expiration:
            return render_template("login.html", error_message="None")
        else:
            return redirect(url_for("views.auth"))

    return render_template("login.html", error_message="None")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    senha = request.form.get("password")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return render_template("login.html", error_message="Email Inexistente")

    if not check_password_hash(usuario.password, senha):
        return render_template("login.html", error_message="Senha invalida")

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


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for("views.home"))


@auth.route("/sign-up", methods=["GET"])
def sign_up_get():
    token = session.get("token")

    if token:
        try:
            dados = jwt.decode(token, get_secret_key(), algorithms="HS256")
            data = dados["expiration"].split(".")[0]

            expiration = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

            if datetime.now() < expiration:
                return redirect(url_for("views.auth"))

        except Exception as e:
            return render_template("cadastroUsuario.html", error_message="None")

    return render_template("cadastroUsuario.html", error_message="None")


@auth.route("/sign-up", methods=["POST"])
def sign_up_post():
    email = request.form.get("email")
    nome = request.form.get("name")
    senha = request.form.get("password")

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        return render_template(
            "cadastroUsuario.html", error_message="Este Usuario Ja Existe"
        )

    if len(nome) < 2:
        return render_template("cadastroUsuario.html", error_message="Nome Invalido")

    if len(senha) < 8:
        return render_template(
            "cadastroUsuario.html", error_message="Sua senha eh mt curta"
        )

    senha_hash = generate_password_hash(senha)

    novo_usuario = Usuario(email=email, nome=nome, password=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

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


@auth.route("/login-google")
def login_oauth():
    google = oauth.create_client("google")
    redirect_url = url_for("auth.authorize", _external=True)
    return google.authorize_redirect(redirect_url)


@auth.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    user = oauth.google.userinfo()
    session["profile"] = user_info

    return redirect(url_for("views.auth"))


@auth.route("/pos")
@token_required
def pos():
    email = dict(session)["profile"]["email"]
    return f"Ola {email}"
