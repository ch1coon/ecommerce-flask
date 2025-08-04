from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Anuncio, Categoria
from .. import db
from flask_login import login_required, current_user

anuncio_bp = Blueprint('anuncio', __name__, template_folder='templates/anuncio')


@anuncio_bp.route('/')
@login_required
def list():
    anuncios = Anuncio.query.filter_by(usuario_id=current_user.id).all()
    return render_template('anuncio/list.html', anuncios=anuncios)


@anuncio_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        a = Anuncio(
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            preco=request.form['preco'],
            usuario_id=current_user.id,
            categoria_id=request.form['categoria']
        )
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('anuncio.list'))
    return render_template('anuncio/form.html', categorias=categorias)
