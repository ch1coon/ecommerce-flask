from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.anuncio import Anuncio
from ..models.compra import Compra

relatorios_bp = Blueprint('relatorios', __name__, template_folder='templates/relatorios')

@relatorios_bp.route('/vendas')
@login_required
def vendas():
    anuncios_vendidos = Anuncio.query.filter_by(usuario_id=current_user.id).all()
    vendas = []
    for anuncio in anuncios_vendidos:
        compras = Compra.query.filter_by(anuncio_id=anuncio.id).all()
        for compra in compras:
            vendas.append({'anuncio': anuncio, 'compra': compra})
    return render_template('relatorios/vendas.html', vendas=vendas)

@relatorios_bp.route('/compras')
@login_required
def compras():
    compras = Compra.query.filter_by(usuario_id=current_user.id).all()
    return render_template('relatorios/compras.html', compras=compras)

