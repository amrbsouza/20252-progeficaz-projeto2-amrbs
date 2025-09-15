def connect_db():
    pass

def get_imoveis():
    conn = connect_db()
    cursor = conn.cursor()
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
    cursor.execute("SELECT * FROM imoveis WHERE id = ?", (imovel_id,))
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
        SET logradouro=?, tipo_logradouro=?, bairro=?, cidade=?, 
            cep=?, tipo=?, valor=?, data_aquisicao=?
        WHERE id=?""", 
        (dados['logradouro'], dados['tipo_logradouro'], dados['bairro'], dados['cidade'], dados['cep'], dados['tipo'], dados['valor'], dados['data_aquisicao'], imovel_id))
    conn.commit()
    return cursor.rowcount  

def remover_imovel_db(imovel_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = ?", (imovel_id,))
    conn.commit()
    return cursor.rowcount 