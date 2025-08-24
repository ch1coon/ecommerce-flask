from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.favorito import Favorito
from ..models.anuncio import Anuncio
from .. import db

favorito_bp = Blueprint('favorito', __name__, template_folder='templates/favorito')

@favorito_bp.route('/')
@login_required
def list_favorito():
    favoritos = Favorito.query.filter_by(usuario_id=current_user.id).all()
    return render_template('favorito/list.html', favoritos=favoritos)

@favorito_bp.route('/add', methods=['POST'])
@login_required
def create_favorito():
    anuncio_id = request.form.get('anuncio_id')
    if not anuncio_id:
        flash('Anúncio inválido.', 'danger')
        return redirect(request.referrer or url_for('favorito.list_favorito'))
    anuncio = Anuncio.query.get(anuncio_id)
    if not anuncio:
        flash('Anúncio não encontrado.', 'danger')
        return redirect(request.referrer or url_for('favorito.list_favorito'))
    existente = Favorito.query.filter_by(usuario_id=current_user.id, anuncio_id=anuncio_id).first()
    if existente:
        flash('Este anúncio já está nos seus favoritos.', 'info')
        return redirect(request.referrer or url_for('favorito.list_favorito'))
    favorito = Favorito(usuario_id=current_user.id, anuncio_id=anuncio_id)
    db.session.add(favorito)
    db.session.commit()
    flash('Anúncio adicionado aos favoritos!', 'success')
    return redirect(request.referrer or url_for('favorito.list_favorito'))

@favorito_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def remover_favorito(id):
    favorito = Favorito.query.get_or_404(id)
    if favorito.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('favorito.list_favorito'))
    db.session.delete(favorito)
    db.session.commit()
    flash('Favorito removido com sucesso!', 'success')
    next_url = request.form.get('next')
    if next_url:
        return redirect(next_url)
    return redirect(url_for('favorito.list_favorito'))
