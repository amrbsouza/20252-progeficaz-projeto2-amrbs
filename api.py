from flask import Flask
import views

app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    return views.listar_imoveis()

@app.route('/imoveis/<int:imovel_id>', methods=['GET'])
def get_imovel_por_id(imovel_id):
    return views.buscar_imovel_por_id(imovel_id)

@app.route('/imoveis/tipo/<string:tipo>', methods=['GET'])
def get_imoveis_por_tipo(tipo):
    return views.listar_imoveis_por_tipo(tipo)

@app.route('/imoveis/cidade/<string:cidade>', methods=['GET'])  
def get_imoveis_por_cidade(cidade):
    return views.listar_imoveis_por_cidade(cidade)

@app.route('/imoveis', methods=['POST'])
def post_imovel():
    return views.adicionar_imovel()

@app.route('/imoveis/<int:imovel_id>', methods=['PUT'])
def atualizar_imovel(imovel_id):
    return views.atualizar_imovel(imovel_id)

@app.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def remover_imovel(imovel_id):
    return views.remover_imovel(imovel_id)
    
    
if __name__ == '__main__':
    app.run(debug=True)