from flask import Blueprint, render_template

resposta_bp = Blueprint('resposta', __name__)

@resposta_bp.route('/')
def listar_respostas():
    # Lista respostas
    return render_template('resposta/list.html')

@resposta_bp.route('/nova')
def nova_resposta():
    # Form para nova resposta
    return render_template('resposta/form.html')
