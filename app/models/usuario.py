from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    anuncios = db.relationship("Anuncio", back_populates="usuario", lazy=True)
    perguntas = db.relationship("Pergunta", back_populates="usuario", lazy=True)
    respostas = db.relationship("Resposta", back_populates="usuario", lazy=True)
    compras = db.relationship("Compra", back_populates="usuario", lazy=True)
    favoritos = db.relationship("Favorito", back_populates="usuario", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"
