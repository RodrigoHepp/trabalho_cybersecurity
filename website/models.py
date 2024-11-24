from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    users = db.relationship("Usuario", back_populates="role")


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

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", back_populates="users")
