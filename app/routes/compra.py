from flask import Blueprint, render_template

compra_bp = Blueprint('compra', __name__)

@compra_bp.route('/')
def listar_compras():
    # Mostrar lista de compras feitas pelo usuário
    return render_template('compra/list.html')

@compra_bp.route('/nova')
def nova_compra():
    # Form para nova compra
    return render_template('compra/form.html')
