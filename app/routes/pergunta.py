from flask import Blueprint, render_template

pergunta_bp = Blueprint('pergunta', __name__)

@pergunta_bp.route('/')
def listar_perguntas():
    # Lista perguntas feitas
    return render_template('pergunta/list.html')

@pergunta_bp.route('/novo')
def nova_pergunta():
    # Form para nova pergunta
    return render_template('pergunta/form.html')
