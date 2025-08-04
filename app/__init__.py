from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login.init_app(app)

    from .routes.auth      import auth_bp
    from .routes.anuncio   import anuncio_bp
    from .routes.pergunta  import pergunta_bp
    from .routes.resposta  import resposta_bp
    from .routes.compra    import compra_bp
    from .routes.favorito  import favorito_bp
    from .routes.categoria import categoria_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(anuncio_bp,   url_prefix='/anuncios')
    app.register_blueprint(pergunta_bp,  url_prefix='/perguntas')
    app.register_blueprint(resposta_bp,  url_prefix='/respostas')
    app.register_blueprint(compra_bp,    url_prefix='/compras')
    app.register_blueprint(favorito_bp,  url_prefix='/favoritos')
    app.register_blueprint(categoria_bp, url_prefix='/categorias')

    return app
