from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Permissao(db.Model):
    __tablename__ = "permissao"

    id = db.Column(db.Integer, primary_key=True)
    permissao_nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    papel_permissao = db.relationship("PapelPermissao", back_populates="permissao")


class Papel(db.Model):
    __tablename__ = "papel"

    id = db.Column(db.Integer, primary_key=True)
    papeis_nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(255))

    papeis_permissoes = db.relationship("PapelPermissao", back_populates="papel")
    usuarios = db.relationship("Usuario", back_populates="papel")


class PapelPermissao(db.Model):
    __tablename__ = "papel_permissao"

    id = db.Column(db.Integer, primary_key=True)
    papeis_id = db.Column(db.Integer, db.ForeignKey("papel.id"), nullable=False)
    permissoes_id = db.Column(db.Integer, db.ForeignKey("permissao.id"), nullable=False)

    papel = db.relationship("Papel", back_populates="papeis_permissoes")
    permissao = db.relationship("Permissao", back_populates="papel_permissao")


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime(timezone=True), default=func.now())
    data_update = db.Column(
        db.DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    papel_id = db.Column(db.Integer, db.ForeignKey("papel.id"))
    papel = db.relationship("Papel", back_populates="usuarios")
    tokens = db.relationship("Token", back_populates="usuario")


class Token(db.Model):
    __tablename__ = "token"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), nullable=False)
    data_expiracao = db.Column(db.DateTime(timezone=True))
    data_criacao = db.Column(db.DateTime(timezone=True), default=func.now())

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    usuario = db.relationship("Usuario", back_populates="tokens")
