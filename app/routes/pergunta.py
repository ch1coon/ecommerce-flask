from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.pergunta import Pergunta
from ..models.anuncio import Anuncio
from .. import db

pergunta_bp = Blueprint('pergunta', __name__, template_folder='templates/pergunta')

@pergunta_bp.route('/')
@login_required
def listar_perguntas():
    perguntas = Pergunta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('pergunta/list.html', perguntas=perguntas)

@pergunta_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_pergunta():
    anuncios = Anuncio.query.all()
    if request.method == 'POST':
        texto = request.form['texto']
        anuncio_id = request.form['anuncio_id']
        pergunta = Pergunta(texto=texto, usuario_id=current_user.id, anuncio_id=anuncio_id)
        db.session.add(pergunta)
        db.session.commit()
        if request.referrer and '/anuncios/publico/' in request.referrer:
            return redirect(url_for('anuncio.publico_detail', id=anuncio_id))
        flash('Pergunta criada com sucesso!', 'success')
        return redirect(url_for('pergunta.listar_perguntas'))
    return render_template('pergunta/form.html', anuncios=anuncios)

@pergunta_bp.route('/<int:id>')
@login_required
def detalhe_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    if pergunta.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('pergunta.listar_perguntas'))
    return render_template('pergunta/detail.html', pergunta=pergunta)

@pergunta_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    if pergunta.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('pergunta.listar_perguntas'))
    anuncios = Anuncio.query.all()
    if request.method == 'POST':
        pergunta.texto = request.form['texto']
        pergunta.anuncio_id = request.form['anuncio_id']
        db.session.commit()
        flash('Pergunta atualizada com sucesso!', 'success')
        return redirect(url_for('pergunta.listar_perguntas'))
    return render_template('pergunta/form.html', pergunta=pergunta, anuncios=anuncios)

@pergunta_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def excluir_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    if pergunta.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('pergunta.listar_perguntas'))
    db.session.delete(pergunta)
    db.session.commit()
    flash('Pergunta excluída com sucesso!', 'success')
    return redirect(url_for('pergunta.listar_perguntas'))
