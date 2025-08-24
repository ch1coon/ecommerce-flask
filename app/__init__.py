from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth      import auth_bp
    from .routes.anuncio   import anuncio_bp
    from .routes.pergunta  import pergunta_bp
    from .routes.resposta  import resposta_bp
    from .routes.compra    import compra_bp
    from .routes.favorito  import favorito_bp
    from .routes.categoria import categoria_bp
    from .routes.usuario   import usuario_bp
    from .routes.relatorios import relatorios_bp
    from .models.usuario import Usuario

    @login.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(anuncio_bp,   url_prefix='/anuncios')
    app.register_blueprint(pergunta_bp,  url_prefix='/perguntas')
    app.register_blueprint(resposta_bp,  url_prefix='/respostas')
    app.register_blueprint(compra_bp,    url_prefix='/compras')
    app.register_blueprint(favorito_bp,  url_prefix='/favoritos')
    app.register_blueprint(categoria_bp, url_prefix='/categorias')
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')
    app.register_blueprint(relatorios_bp, url_prefix='/relatorios')

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html', usuario=current_user)

    return app
