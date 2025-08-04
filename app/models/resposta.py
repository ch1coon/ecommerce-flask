from datetime import datetime

from app import db


class Resposta(db.Model):
    __tablename__ = "resposta"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pergunta_id = db.Column(db.Integer, db.ForeignKey("pergunta.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    def __repr__(self):
        return f"<Resposta {self.id}>"
