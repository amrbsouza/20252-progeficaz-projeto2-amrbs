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