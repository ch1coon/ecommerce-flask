from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required
from ..models.usuario import Usuario
from .. import db

usuario_bp = Blueprint('usuario', __name__, template_folder='templates/usuario')

@usuario_bp.route('/')
@login_required
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuario/list.html', usuarios=usuarios)

@usuario_bp.route('/create', methods=['GET', 'POST'])
@login_required
def criar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('usuario.criar_usuario'))
        usuario = Usuario()
        usuario.nome = nome
        usuario.email = email
        usuario.senha_hash = generate_password_hash(senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('usuario.listar_usuarios'))
    return render_template('usuario/form.html')

@usuario_bp.route('/<int:id>')
@login_required
def detalhe_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('usuario/detail.html', usuario=usuario)

@usuario_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        email = request.form['email']
        if Usuario.query.filter(Usuario.email == email, Usuario.id != id).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('usuario.editar_usuario', id=id))
        usuario.email = email
        senha = request.form.get('senha')
        if senha:
            usuario.senha_hash = generate_password_hash(senha)
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuario.listar_usuarios'))
    return render_template('usuario/form.html', usuario=usuario)

@usuario_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('usuario.listar_usuarios'))
