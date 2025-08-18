from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from ..models.categoria import Categoria
from .. import db

categoria_bp = Blueprint('categoria', __name__, template_folder='templates/categoria')

@categoria_bp.route('/')
@login_required
def list_categoria():
    categorias = Categoria.query.all()
    return render_template('categoria/list.html', categorias=categorias)

@categoria_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        if Categoria.query.filter_by(nome=nome).first():
            flash('Categoria já existe!', 'danger')
            return redirect(url_for('categoria.create_categoria'))
        categoria = Categoria(nome=nome)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoria criada com sucesso!', 'success')
        return redirect(url_for('categoria.list_categoria'))
    return render_template('categoria/form.html')

@categoria_bp.route('/<int:id>')
@login_required
def get_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return render_template('categoria/get_categoria.html', categoria=categoria)

@categoria_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form['nome']
        if Categoria.query.filter(Categoria.nome == nome, Categoria.id != id).first():
            flash('Já existe uma categoria com esse nome!', 'danger')
            return redirect(url_for('categoria.update_categoria', id=id))
        categoria.nome = nome
        db.session.commit()
        flash('Categoria atualizada com sucesso!', 'success')
        return redirect(url_for('categoria.list_categoria'))
    return render_template('categoria/form.html', categoria=categoria)

@categoria_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    if categoria.anuncios:
        flash('Não é possível excluir uma categoria com anúncios vinculados.', 'danger')
        return redirect(url_for('categoria.list_categoria'))
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('categoria.list_categoria'))
