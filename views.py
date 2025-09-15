from flask import jsonify, request
from utils import get_imoveis, get_imovel_por_id, adicionar_imovel_db, atualizar_imovel_db, remover_imovel_db

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

def adicionar_imovel():
    """POST /imoveis - Adiciona um novo imóvel"""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    novo_id = adicionar_imovel_db(dados)
    
    response = dados.copy()
    response['id'] = novo_id
    
    return jsonify(response), 201

def atualizar_imovel(imovel_id):
    """PUT /imoveis/<id> - Atualiza um imóvel existente"""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    
    linhas_afetadas = atualizar_imovel_db(imovel_id, dados)
    if linhas_afetadas > 0:
        response = dados.copy()
        response['id'] = imovel_id
        return jsonify(response), 200
    
    return jsonify({'erro': 'Imóvel não encontrado'}), 404

def remover_imovel(imovel_id):
    """DELETE /imoveis/<id> - Remove um imóvel existente"""
    linhas_afetadas = remover_imovel_db(imovel_id)
    if linhas_afetadas > 0:
        return '', 204  
    return jsonify({'erro': 'Imóvel não encontrado'}), 404