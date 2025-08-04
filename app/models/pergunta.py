from datetime import datetime

from app import db


class Pergunta(db.Model):
    __tablename__ = "pergunta"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)

    resposta = db.relationship("Resposta", uselist=False, backref="pergunta")

    def __repr__(self):
        return f"<Pergunta {self.id}>"
