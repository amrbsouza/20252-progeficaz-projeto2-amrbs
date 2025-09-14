from flask import Flask
import views

app = Flask(__name__)

@app.route('/imoveis', methods=['GET'])
def get_imoveis():
    return views.listar_imoveis()

@app.route('/imoveis/<int:imovel_id>', methods=['GET'])
def get_imovel_por_id(imovel_id):
    return views.buscar_imovel_por_id(imovel_id)
    
if __name__ == '__main__':
    app.run(debug=True)