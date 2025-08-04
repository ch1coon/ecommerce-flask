from datetime import datetime

from app import db


class Anuncio(db.Model):
    __tablename__ = "anuncio"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    perguntas = db.relationship("Pergunta", backref="anuncio", lazy=True)
    compras = db.relationship("Compra", backref="anuncio", lazy=True)
    favoritos = db.relationship("Favorito", backref="anuncio", lazy=True)

    def __repr__(self):
        return f"<Anuncio {self.titulo} - R${self.preco}>"
