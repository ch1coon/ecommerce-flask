from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.compra import Compra
from ..models.anuncio import Anuncio
from .. import db

compra_bp = Blueprint('compra', __name__, template_folder='templates/compra')

@compra_bp.route('/')
@login_required
def listar_compras():
    compras = Compra.query.filter_by(usuario_id=current_user.id).all()
    return render_template('compra/list.html', compras=compras)

@compra_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_compra():
    anuncios = Anuncio.query.filter(Anuncio.usuario_id != current_user.id).all()
    if request.method == 'POST':
        anuncio_id = request.form['anuncio_id']
        anuncio = Anuncio.query.get(anuncio_id)
        if not anuncio:
            flash('Anúncio inválido.', 'danger')
            return redirect(request.referrer or url_for('compra.nova_compra'))
        if anuncio.usuario_id == current_user.id:
            flash('Você não pode comprar o seu próprio anúncio.', 'danger')
            return redirect(request.referrer or url_for('compra.nova_compra'))
        valor_pago = request.form.get('valor_pago', anuncio.preco)
        compra = Compra(
            usuario_id=current_user.id,
            anuncio_id=anuncio.id,
            valor_pago=valor_pago
        )
        db.session.add(compra)
        db.session.commit()
        flash('Compra realizada com sucesso!', 'success')
        return redirect(url_for('compra.listar_compras'))
    return render_template('compra/form.html', anuncios=anuncios)

@compra_bp.route('/<int:id>')
@login_required
def detalhe_compra(id):
    compra = Compra.query.get_or_404(id)
    if compra.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('compra.listar_compras'))
    return render_template('compra/detail.html', compra=compra)

@compra_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editar_compra(id):
    compra = Compra.query.get_or_404(id)
    if compra.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('compra.listar_compras'))
    anuncios = Anuncio.query.filter(Anuncio.usuario_id != current_user.id).all()
    if request.method == 'POST':
        anuncio_id = request.form['anuncio_id']
        anuncio = Anuncio.query.get(anuncio_id)
        if not anuncio:
            flash('Anúncio inválido.', 'danger')
            return redirect(url_for('compra.editar_compra', id=id))
        compra.anuncio_id = anuncio.id
        compra.valor_pago = request.form.get('valor_pago', anuncio.preco)
        db.session.commit()
        flash('Compra atualizada com sucesso!', 'success')
        return redirect(url_for('compra.listar_compras'))
    return render_template('compra/form.html', compra=compra, anuncios=anuncios)

@compra_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def excluir_compra(id):
    compra = Compra.query.get_or_404(id)
    if compra.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('compra.listar_compras'))
    db.session.delete(compra)
    db.session.commit()
    flash('Compra excluída com sucesso!', 'success')
    return redirect(url_for('compra.listar_compras'))
