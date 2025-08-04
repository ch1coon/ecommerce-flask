from flask import Blueprint, render_template

favorito_bp = Blueprint('favorito', __name__)

@favorito_bp.route('/')
def listar_favoritos():
    # Lista produtos favoritos do usuário
    return render_template('favorito/list.html')
