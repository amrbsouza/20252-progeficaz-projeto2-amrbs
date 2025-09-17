from flask import jsonify, request
from utils import get_imoveis, get_imovel_por_id, adicionar_imovel_db, atualizar_imovel_db, remover_imovel_db, adiciona_hateoas_link, adiciona_hateoas_em_lista

def listar_imoveis():
    """GET /imoveis - Lista todos os imóveis"""
    cidade = request.args.get('cidade')
    tipo = request.args.get('tipo')
    imoveis = get_imoveis(cidade=cidade, tipo=tipo)
    
    if not imoveis:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    result = adiciona_hateoas_em_lista(imoveis)
    return jsonify(result)

def buscar_imovel_por_id(imovel_id):
    """GET /imoveis/<id> - Busca imóvel por ID"""
    imovel = get_imovel_por_id(imovel_id)
    
    if imovel:
        imovel_com_links = adiciona_hateoas_link(imovel)
        return jsonify(imovel_com_links)
    
    return jsonify({'erro': 'Imóvel não encontrado'}), 404

def adicionar_imovel():
    """POST /imoveis - Adiciona um novo imóvel"""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    novo_id = adicionar_imovel_db(dados)
    
    response = dados.copy()
    response['id'] = novo_id
    
    response_com_links = adiciona_hateoas_link(response)
    return jsonify(response_com_links), 201

def atualizar_imovel(imovel_id):
    """PUT /imoveis/<id> - Atualiza um imóvel existente"""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    
    linhas_afetadas = atualizar_imovel_db(imovel_id, dados)
    if linhas_afetadas > 0:
        response = dados.copy()
        response['id'] = imovel_id
        
        response_com_links = adiciona_hateoas_link(response)
        return jsonify(response_com_links), 200
    
    return jsonify({'erro': 'Imóvel não encontrado'}), 404

def remover_imovel(imovel_id):
    """DELETE /imoveis/<id> - Remove um imóvel existente"""
    linhas_afetadas = remover_imovel_db(imovel_id)
    if linhas_afetadas > 0:
        return '', 204  
    return jsonify({'erro': 'Imóvel não encontrado'}), 404

def listar_imoveis_por_tipo(tipo):
    """GET /imoveis/tipo/<tipo> - rota para imóveis por tipo específico"""
    imoveis = get_imoveis(tipo=tipo)
    
    if not imoveis:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    result = adiciona_hateoas_em_lista(imoveis)
    result['_links']['self'] = f'/imoveis/tipo/{tipo}'
    return jsonify(result)

def listar_imoveis_por_cidade(cidade):
    """GET /imoveis/cidade/<cidade> - rota para imóveis por cidade específica"""
    imoveis = get_imoveis(cidade=cidade)
    
    if not imoveis:
        return {"erro": "Nenhum imóvel encontrado"}, 404
    
    result = adiciona_hateoas_em_lista(imoveis)
    result['_links']['self'] = f'/imoveis/cidade/{cidade}'
    return jsonify(result)