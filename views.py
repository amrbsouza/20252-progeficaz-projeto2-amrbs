from flask import jsonify
from utils import get_imoveis, get_imovel_por_id

def listar_imoveis():
    """GET /imoveis - Lista todos os imóveis"""
    imoveis = get_imoveis()
    
    if not imoveis:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    return jsonify({'imoveis': imoveis})

def buscar_imovel_por_id(imovel_id):
    """GET /imoveis/<id> - Busca imóvel por ID"""
    imovel = get_imovel_por_id(imovel_id)
    
    if imovel:
        return jsonify(imovel)
    
    return jsonify({'erro': 'Imóvel não encontrado'}), 404