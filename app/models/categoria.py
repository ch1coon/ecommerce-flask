from app import db
from .usuario import Usuario

class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    criado_por = db.relationship("Usuario", backref="categorias_criadas", lazy=True)
    anuncios = db.relationship("Anuncio", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"
