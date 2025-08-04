from flask import Blueprint, render_template

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/')
def listar_categorias():
    # Lista todas categorias
    return render_template('categoria/list.html')
