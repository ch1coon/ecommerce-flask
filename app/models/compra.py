from datetime import datetime

from app import db


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True)
    valor_pago = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)

    def __repr__(self):
        return f"<Compra {self.id} - R${self.valor_pago}>"
