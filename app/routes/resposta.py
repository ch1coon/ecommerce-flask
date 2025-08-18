from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.resposta import Resposta
from ..models.pergunta import Pergunta
from .. import db

resposta_bp = Blueprint('resposta', __name__, template_folder='templates/resposta')

@resposta_bp.route('/')
@login_required
def listar_respostas():
    respostas = Resposta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('resposta/list.html', respostas=respostas)

@resposta_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_resposta():
    perguntas = Pergunta.query.all()
    if request.method == 'POST':
        texto = request.form['texto']
        pergunta_id = request.form['pergunta_id']
        pergunta = Pergunta.query.get(pergunta_id)
        if not pergunta:
            flash('Pergunta inválida.', 'danger')
            return redirect(url_for('resposta.listar_respostas'))
        anuncio = pergunta.anuncio
        if anuncio.usuario_id != current_user.id:
            flash('Apenas o dono do anúncio pode responder esta pergunta.', 'danger')
            return redirect(url_for('resposta.listar_respostas'))
        resposta = Resposta(texto=texto, usuario_id=current_user.id, pergunta_id=pergunta_id)
        db.session.add(resposta)
        db.session.commit()
        flash('Resposta criada com sucesso!', 'success')
        return redirect(url_for('resposta.listar_respostas'))
    return render_template('resposta/form.html', perguntas=perguntas)

@resposta_bp.route('/<int:id>')
@login_required
def detalhe_resposta(id):
    resposta = Resposta.query.get_or_404(id)
    if resposta.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('resposta.listar_respostas'))
    return render_template('resposta/detail.html', resposta=resposta)

@resposta_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editar_resposta(id):
    resposta = Resposta.query.get_or_404(id)
    pergunta = Pergunta.query.get(resposta.pergunta_id)
    anuncio = pergunta.anuncio
    if anuncio.usuario_id != current_user.id:
        flash('Apenas o dono do anúncio pode editar esta resposta.', 'danger')
        return redirect(url_for('resposta.listar_respostas'))
    perguntas = Pergunta.query.all()
    if request.method == 'POST':
        resposta.texto = request.form['texto']
        resposta.pergunta_id = request.form['pergunta_id']
        db.session.commit()
        flash('Resposta atualizada com sucesso!', 'success')
        return redirect(url_for('resposta.listar_respostas'))
    return render_template('resposta/form.html', resposta=resposta, perguntas=perguntas)

@resposta_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def excluir_resposta(id):
    resposta = Resposta.query.get_or_404(id)
    if resposta.usuario_id != current_user.id:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('resposta.listar_respostas'))
    db.session.delete(resposta)
    db.session.commit()
    flash('Resposta excluída com sucesso!', 'success')
    return redirect(url_for('resposta.listar_respostas'))
