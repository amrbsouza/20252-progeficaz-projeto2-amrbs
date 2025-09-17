import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv('.cred')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}

def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None

def get_imoveis(cidade=None, tipo=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    if cidade and tipo:
        cursor.execute("SELECT * FROM imoveis WHERE cidade = %s AND tipo = %s", (cidade, tipo))
    elif cidade:
        cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    elif tipo:
        cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    else:
        cursor.execute("SELECT * FROM imoveis")
    results = cursor.fetchall()
    
    if not results:
        cursor.close()
        conn.close()
        return None
    
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
     
    cursor.close()
    conn.close()
    return imoveis

def get_imovel_por_id(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
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
        cursor.close()
        conn.close()
        return imovel
    
    cursor.close()
    conn.close()
    return None

def adicionar_imovel_db(dados):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        dados['logradouro'],
        dados['tipo_logradouro'], 
        dados['bairro'],
        dados['cidade'],
        dados['cep'],
        dados['tipo'],
        dados['valor'],
        dados['data_aquisicao']
    ))
    conn.commit()
    novo_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    return novo_id

def atualizar_imovel_db(imovel_id, dados):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE imoveis 
        SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s, 
            cep=%s, tipo=%s, valor=%s, data_aquisicao=%s
        WHERE id=%s""", 
        (dados['logradouro'], dados['tipo_logradouro'], dados['bairro'], dados['cidade'], dados['cep'], dados['tipo'], dados['valor'], dados['data_aquisicao'], imovel_id))
    conn.commit()
    linhas_alteradas = cursor.rowcount
    
    cursor.close()
    conn.close()
    return linhas_alteradas

def remover_imovel_db(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
    conn.commit()
    linhas_excluidas = cursor.rowcount
    
    cursor.close()
    conn.close()
    return linhas_excluidas

def adiciona_hateoas_link(imovel):
    """Adiciona link HATEOAS para um imóvel"""
    imovel_id = imovel['id']
    imovel['_links'] = {
        'self': f'/imoveis/{imovel_id}',
        'update': f'/imoveis/{imovel_id}',
        'delete': f'/imoveis/{imovel_id}',
        'all': '/imoveis',
        'by_type': f"/imoveis/tipo/{imovel['tipo']}",
        'by_city': f"/imoveis/cidade/{imovel['cidade']}"
    }
    return imovel

def adiciona_hateoas_em_lista(imoveis_list):
    """Adiciona links HATEOAS para uma coleção de imóveis"""
    result = {
        'imoveis': [adiciona_hateoas_link(imovel) for imovel in imoveis_list],
        '_links': {
            'self': '/imoveis',
            'create': '/imoveis'
        }
    }
    return result