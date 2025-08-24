from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.usuario import Usuario
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if not usuario:
                return {'success': False, 'error': 'E-mail não cadastrado.'}, 400
            if not check_password_hash(usuario.senha_hash, senha):
                return {'success': False, 'error': 'Senha incorreta.'}, 401
            login_user(usuario)
            return {'success': True, 'redirect': url_for('dashboard')}
        else:
            if usuario and check_password_hash(usuario.senha_hash, senha):
                login_user(usuario)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('E-mail ou senha inválidos.', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('auth.register'))
        usuario = Usuario()
        usuario.nome = nome
        usuario.email = email
        usuario.senha_hash = generate_password_hash(senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))
