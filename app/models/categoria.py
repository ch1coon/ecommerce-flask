from app import db

class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    anuncios = db.relationship("Anuncio", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"
