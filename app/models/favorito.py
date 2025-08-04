from datetime import datetime

from app import db


class Favorito(db.Model):
    __tablename__ = "favorito"

    id = db.Column(db.Integer, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)

    def __repr__(self):
        return f"<Favorito anuncio={self.anuncio_id} usuario={self.usuario_id}>"
