from flask import Flask, jsonify

app = Flask(__name__)

def connect_db():
    pass

@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    conn = connect_db()
    cursor = conn.cursor()
    results = cursor.fetchall()
    
    imoveis = []
    for row in results:
        imovel = {
            'id': row[0],
            'logradouro': row[1],
            'tipo_logradouro': row[2],
            'bairro': row[3],
            'cidade': row[4],
            'cep': row[5],
            'tipo': row[6],
            'valor': row[7],
            'data_aquisicao': row[8]
        }
        imoveis.append(imovel)
    
    return jsonify({'imoveis': imoveis})

@app.route('/imoveis/<int:imovel_id>', methods=['GET'])
def get_imovel_por_id(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()
    result = cursor.fetchone()  
    
    if result:
        imovel = {
            'id': result[0],
            'logradouro': result[1],
            'tipo_logradouro': result[2],
            'bairro': result[3],
            'cidade': result[4],
            'cep': result[5],
            'tipo': result[6],
            'valor': result[7],
            'data_aquisicao': result[8]
        }
        return jsonify(imovel)
    
    return jsonify({'error': 'Imóvel não encontrado'}), 404