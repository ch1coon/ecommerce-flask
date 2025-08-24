from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Anuncio, Categoria
from .. import db
from flask_login import login_required, current_user

anuncio_bp = Blueprint('anuncio', __name__, template_folder='templates/anuncio')


@anuncio_bp.route('/')
@login_required
def list_anuncio():
    anuncios = Anuncio.query.filter_by(usuario_id=current_user.id).all()
    return render_template('anuncio/list.html', anuncios=anuncios)


@anuncio_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_anuncio():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        preco_str = request.form['preco'].replace('.', '').replace(',', '.')
        try:
            preco = float(preco_str)
        except ValueError:
            preco = 0.0
        if preco <= 0:
            flash('O valor do anúncio deve ser maior que zero.', 'danger')

            return render_template('anuncio/form.html', categorias=categorias, form=request.form)
        a = Anuncio(
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            preco=preco,
            usuario_id=current_user.id,
            categoria_id=request.form['categoria']
        )
        db.session.add(a)
        db.session.commit()
        flash('Anúncio criado com sucesso!', 'success')
        return redirect(url_for('anuncio.list_anuncio'))
    return render_template('anuncio/form.html', categorias=categorias)


@anuncio_bp.route('/<int:id>')
@login_required
def get_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id == current_user.id:
        return redirect(url_for('anuncio.publico_detail', id=anuncio.id))
    return redirect(url_for('anuncio.explorar_anuncios'))


@anuncio_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def update_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id != current_user.id:
        return redirect(url_for('anuncio.list_anuncio'))
    categorias = Categoria.query.all()
    if request.method == 'POST':
        preco_str = request.form['preco'].replace('.', '').replace(',', '.')
        try:
            preco = float(preco_str)
        except ValueError:
            preco = 0.0
        anuncio.titulo = request.form['titulo']
        anuncio.descricao = request.form['descricao']
        anuncio.preco = preco
        anuncio.categoria_id = request.form['categoria']
        db.session.commit()
        flash('Anúncio editado com sucesso!', 'success')
        return redirect(url_for('anuncio.list_anuncio'))
    return render_template('anuncio/form.html', anuncio=anuncio, categorias=categorias)


@anuncio_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id != current_user.id:
        return redirect(url_for('anuncio.list_anuncio'))
    db.session.delete(anuncio)
    db.session.commit()
    flash('Anúncio deletado com sucesso!', 'success')
    return redirect(url_for('anuncio.list_anuncio'))


@anuncio_bp.route('/explorar')
def explorar_anuncios():
    from flask import request
    from flask_login import current_user
    categorias = Categoria.query.all()
    categoria_id = request.args.get('categoria', type=int)
    favoritos_only = request.args.get('favoritos', type=int) == 1
    anuncios_query = Anuncio.query
    if categoria_id:
        anuncios_query = anuncios_query.filter_by(categoria_id=categoria_id)
    if favoritos_only and current_user.is_authenticated:
        from ..models.favorito import Favorito
        favoritos_ids = [f.anuncio_id for f in Favorito.query.filter_by(usuario_id=current_user.id).all()]
        anuncios_query = anuncios_query.filter(Anuncio.id.in_(favoritos_ids))
    anuncios = anuncios_query.all()
    return render_template('anuncio/explorar.html', anuncios=anuncios, categorias=categorias, categoria_id=categoria_id, favoritos_only=favoritos_only)


@anuncio_bp.route('/publico/<int:id>')
def publico_detail(id):
    anuncio = Anuncio.query.get_or_404(id)
    perguntas = anuncio.perguntas
    perguntas_respostas = []
    for pergunta in perguntas:
        perguntas_respostas.append({
            'pergunta': pergunta,
            'resposta': getattr(pergunta, 'resposta', None)
        })

    is_favorito = False
    favorito_id = None
    if current_user.is_authenticated:
        from ..models.favorito import Favorito
        favorito = Favorito.query.filter_by(usuario_id=current_user.id, anuncio_id=anuncio.id).first()
        if favorito:
            is_favorito = True
            favorito_id = favorito.id
    return render_template('anuncio/publico_detail.html', anuncio=anuncio, perguntas_respostas=perguntas_respostas, is_favorito=is_favorito, favorito_id=favorito_id)


@anuncio_bp.route('/<int:anuncio_id>/responder/<int:pergunta_id>', methods=['POST'])
@login_required
def responder_pergunta(anuncio_id, pergunta_id):
    anuncio = Anuncio.query.get_or_404(anuncio_id)
    if anuncio.usuario_id != current_user.id:
        return redirect(url_for('anuncio.publico_detail', id=anuncio_id))
    pergunta = next((p for p in anuncio.perguntas if p.id == pergunta_id), None)
    if not pergunta:
        return redirect(url_for('anuncio.publico_detail', id=anuncio_id))
    texto = request.form['texto']
    if hasattr(pergunta, 'resposta') and pergunta.resposta:
        return redirect(url_for('anuncio.publico_detail', id=anuncio_id))
    from ..models.resposta import Resposta
    resposta = Resposta(texto=texto, usuario_id=current_user.id, pergunta_id=pergunta_id)
    db.session.add(resposta)
    db.session.commit()
    return redirect(url_for('anuncio.publico_detail', id=anuncio_id))
