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
    
    return imoveis

def get_imovel_por_id(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
    result = cursor.fetchone()
    
    if result:
        return {
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
    return cursor.lastrowid

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
    return cursor.rowcount  

def remover_imovel_db(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
    conn.commit()
    return cursor.rowcount 