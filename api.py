from flask import Flask
import views

app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    return views.listar_imoveis()

@app.route('/imoveis/<int:imovel_id>', methods=['GET'])
def get_imovel_por_id(imovel_id):
    return views.buscar_imovel_por_id(imovel_id)

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