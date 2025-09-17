import pytest
from unittest.mock import patch, MagicMock
from api import app
from utils import connect_db


@pytest.fixture
def client():
    """Cliente de teste para a API. Ele simula um usuário da API de imóveis."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# GET - Todos os imóveis + atributos
@patch("utils.connect_db")  # Substitui-se a função que conecta ao banco por um Mock
def test_get_imoveis(mock_connect_db, client):
    """Testa a rota /imoveis - deve retornar uma lista de imóveis."""

    # GIVEN/GEGEBEN 
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (0, 'Rua Inhambu, 97 ', 'Rua', 'Moema', 'São Paulo', '04520-010', 'Apartamento', 7000000.0, '2022-06-02'),
        (1, 'Rua Nascimento Silva, 107', 'Rua', 'Ipanema', 'Rio de Janeiro', '22421-025', 'Casa', 5000000.0, '1974-01-25'),
        (2, 'Praça dos Três Poderes', 'Praça', 'Centro', 'Brasília', '70175-900', 'Palácio', 200000000.0, '1960-04-21'), 
        (3, 'Avenida Braz Leme, 1981', 'Avenida', 'Santana', 'São Paulo', '02022-010', 'Apartamento', 1800000.0, '2014-10-27')
    ]
    mock_connect_db.return_value = mock_conn

    # WHEN/WANN 
    response = client.get('/imoveis')

    # THEN/DANN
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'imoveis' in response_data
    assert '_links' in response_data
    assert len(response_data['imoveis']) == 4
    
    expected_imoveis = [
        {'id': 0, 'logradouro': 'Rua Inhambu, 97 ', 'tipo': 'Apartamento', 'cidade': 'São Paulo'},
        {'id': 1, 'logradouro': 'Rua Nascimento Silva, 107', 'tipo': 'Casa', 'cidade': 'Rio de Janeiro'},
        {'id': 2, 'logradouro': 'Praça dos Três Poderes', 'tipo': 'Palácio', 'cidade': 'Brasília'},
        {'id': 3, 'logradouro': 'Avenida Braz Leme, 1981', 'tipo': 'Apartamento', 'cidade': 'São Paulo'}
    ]

    for i, expected in enumerate(expected_imoveis):
        imovel = response_data['imoveis'][i]
        assert imovel['id'] == expected['id']
        assert imovel['logradouro'] == expected['logradouro']
        assert imovel['tipo'] == expected['tipo']
        assert imovel['cidade'] == expected['cidade']
        assert '_links' in imovel  
 
    collection_links = response_data['_links']
    assert 'self' in collection_links
    assert 'create' in collection_links

 # GET - Quando não há imóveis no banco de dados
@patch("utils.connect_db")
def test_get_imoveis_vazio(mock_connect_db, client):
    """Testa a rota /imoveis quando o banco de dados não tem imóveis."""

    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    mock_connect_db.return_value = mock_conn

    # WHEN/WANN 
    response = client.get('/imoveis')

    # THEN/DANN 
    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Nenhum imóvel encontrado'}
    
    
# GET - Imóvel por ID  com suas características concernentes
@patch("utils.connect_db")
def test_get_imovel_por_id(mock_connect_db, client):
    """Teste da rota /imoveis/<id> - que deve retornar um imóvel específico."""

    # GIVEN/GEGEBEN 
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, 'Rua Nascimento Silva, 107', 'Rua', 'Ipanema', 
        'Rio de Janeiro', '22421-025', 'Casa', 5000000.0, '1974-01-25'
    )
    mock_connect_db.return_value = mock_conn

    # WHEN/WANN
    response = client.get('/imoveis/1')

    # THEN/DANN
    assert response.status_code == 200
    expected_response = {
        'id': 1,
        'logradouro': 'Rua Nascimento Silva, 107',
        'tipo_logradouro': 'Rua',
        'bairro': 'Ipanema',
        'cidade': 'Rio de Janeiro',
        'cep': '22421-025',
        'tipo': 'Casa',
        'valor': 5000000.0,
        'data_aquisicao': '1974-01-25',
        '_links': {
            'self': '/imoveis/1',
            'update': '/imoveis/1',
            'delete': '/imoveis/1',
            'all': '/imoveis',
            'by_type': '/imoveis/tipo/Casa',
            'by_city': '/imoveis/cidade/Rio de Janeiro'
        }
    }
    assert response.get_json() == expected_response
 
 # GET - Imóvel por ID não encontrado 
@patch("utils.connect_db")
def test_get_imovel_nao_encontrado(mock_connect_db, client):
    """Testa a rota /imoveis/<id> quando o imóvel não existe"""

    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_connect_db.return_value = mock_conn

    # WHEN/WANN
    response = client.get('/imoveis/99999999999')

    # THEN/DANN
    assert response.status_code == 404
    expected_response = {
        'erro': 'Imóvel não encontrado'
    }
    assert response.get_json() == expected_response
    
# POST - Adicionar um imóvel
@patch("utils.connect_db")
def test_post_adicionar_imovel(mock_connect_db, client):
    """Testa a rota /imoveis para adicionar um novo imóvel"""
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 4  # ID do novo imóvel criado
    mock_connect_db.return_value = mock_conn
    novo_imovel = {
        'logradouro': 'Rua Dr Getúlio Vargas, 308',
        'tipo_logradouro': 'Rua',
        'bairro': 'Centro',
        'cidade': 'Ituverava',
        'cep': '14500-000',
        'tipo': 'Casa',
        'valor': 1000000.0,
        'data_aquisicao': '1968-02-15'
    }

    # WHEN/WANN
    response = client.post('/imoveis', json=novo_imovel, content_type='application/json')

    # THEN/DANN
    assert response.status_code == 201
    expected_response = {
        'id': 4,
        'logradouro': 'Rua Dr Getúlio Vargas, 308',
        'tipo_logradouro': 'Rua',
        'bairro': 'Centro',
        'cidade': 'Ituverava',
        'cep': '14500-000',
        'tipo': 'Casa',
        'valor': 1000000.0,
        'data_aquisicao': '1968-02-15',
        '_links': {
            'self': '/imoveis/4',
            'update': '/imoveis/4',
            'delete': '/imoveis/4',
            'all': '/imoveis',
            'by_type': '/imoveis/tipo/Casa',
            'by_city': '/imoveis/cidade/Ituverava'
        } 
    }
    assert response.get_json() == expected_response

# PUT - Atualiza um imóvel que já existe 
@patch("utils.connect_db")
def test_put_atualizar_imovel(mock_connect_db, client):
    """Testa a atualização de um imóvel existente pela rota /imoveis/<id>"""
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        1, 'Rua Nascimento Silva, 107', 'Rua', 'Ipanema', 
        'Rio de Janeiro', '22421-025', 'Casa', 5000000.0, '1974-01-25'
    )
    mock_cursor.rowcount = 1
    mock_connect_db.return_value = mock_conn
    dados_atualizados = {
        'logradouro': 'Rua Nascimento Silva, 107',
        'tipo_logradouro': 'Rua',
        'bairro': 'Ipanema',
        'cidade': 'Rio de Janeiro',
        'cep': '22421-025',
        'tipo': 'Casa',
        'valor': 13000000.0,  
        'data_aquisicao': '1974-01-25'
    }
    
    # WHEN/WANN
    response = client.put('/imoveis/1', json=dados_atualizados)
    
    # THEN/DANN
    assert response.status_code == 200
    expected_response = {
        'id': 1,
        'logradouro': 'Rua Nascimento Silva, 107',
        'tipo_logradouro': 'Rua',
        'bairro': 'Ipanema',
        'cidade': 'Rio de Janeiro',
        'cep': '22421-025',
        'tipo': 'Casa',
        'valor': 13000000.0,
        'data_aquisicao': '1974-01-25',
        '_links': {
            'self': '/imoveis/1',
            'update': '/imoveis/1',
            'delete': '/imoveis/1',
            'all': '/imoveis',
            'by_type': '/imoveis/tipo/Casa',
            'by_city': '/imoveis/cidade/Rio de Janeiro'
        }
    }
    assert response.get_json() == expected_response

# PUT - Atualiza um imóvel inexistente 
@patch("utils.connect_db")
def test_put_atualizar_imovel_inexistente(mock_connect_db, client):
    """Testa atualização de um imóvel inexistente""" 
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0  
    mock_connect_db.return_value = mock_conn
    
    dados_atualizados = {
        'logradouro': 'Rua Pindamonhangaba, 13',
        'tipo_logradouro': 'Rua',
        'bairro': 'Centro',
        'cidade': 'Pindamonhangaba',
        'cep': '13450-000',
        'tipo': 'Casa',
        'valor': 50.0,
        'data_aquisicao': '1989-12-13'
    }
    
    # WHEN/WANN
    response = client.put('/imoveis/99999', json=dados_atualizados)
    
    # THEN/DANN
    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Imóvel não encontrado'}
    
# DELETE - Deleta um ímovel 
@patch("utils.connect_db")
def test_delete_remove_imovel(mock_connect_db, client):
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (
        5, 'Rua Oscar Freire, 103', 'Rua', 'Cerqueira César', 
        'São Paulo', '01426-000', 'Apartamento', 15000000.0, '2006-06-10'
    )
    mock_cursor.rowcount = 1
    mock_connect_db.return_value = mock_conn
    
    # WHEN/WANN
    response = client.delete('/imoveis/5')
    
    # THEN/DANN
    assert response.status_code == 204
    assert response.data == b''
    
# DELETE - Deleta um imóvel inexistente
@patch("utils.connect_db")
def test_delete_remove_imovel_inexistente(mock_connect_db, client):
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    mock_connect_db.return_value = mock_conn
    
    # WHEN/WANN
    response = client.delete('/imoveis/1989999999')
    
    # THEN/DANN
    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Imóvel não encontrado'}
    
# GET - Filtro por tipo de imóvel e cidade    
@patch("utils.connect_db")
def test_get_imoveis_filtro_tipo(mock_connect_db, client):
    """Testa filtro por tipo"""
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Rua Nascimento Silva, 107', 'Rua', 'Ipanema', 'Rio de Janeiro', '22421-025', 'Casa', 5000000.0, '1974-01-25')
    ]
    mock_connect_db.return_value = mock_conn
    
    # WHEN/WANN
    response = client.get('/imoveis?tipo=Casa')
    
    # THEN/DANN
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'imoveis' in response_data
    assert '_links' in response_data
    assert len(response_data['imoveis']) == 1
    assert response_data['imoveis'][0]['tipo'] == 'Casa'
    for imovel in response_data['imoveis']:
        assert '_links' in imovel
    
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM imoveis WHERE tipo = %s", 
        ("Casa",)
    )

@patch("utils.connect_db")
def test_get_imoveis_filtro_cidade(mock_connect_db, client):
    """Testa filtro por cidade"""

    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (0, 'Rua Inhambu, 97 ', 'Rua', 'Moema', 'São Paulo', '04520-010', 'Apartamento', 7000000.0, '2022-06-02'),
        (3, 'Avenida Braz Leme, 1981', 'Avenida', 'Santana', 'São Paulo', '02022-010', 'Apartamento', 1800000.0, '2014-10-27')
    ]
    mock_connect_db.return_value = mock_conn
    
    # WHEN/WANN
    response = client.get('/imoveis?cidade=São Paulo')
    
    # THEN/DANN
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'imoveis' in response_data
    assert '_links' in response_data
    assert len(response_data['imoveis']) == 2
    assert response_data['imoveis'][0]['cidade'] == 'São Paulo'
    assert response_data['imoveis'][1]['cidade'] == 'São Paulo'
    for imovel in response_data['imoveis']:
        assert '_links' in imovel
    
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM imoveis WHERE cidade = %s", 
        ("São Paulo",)
    )

@patch("utils.connect_db")
def test_get_imoveis_filtro_tipo_rota_separada(mock_connect_db, client):
    """Testa filtragem por uma rota separada"""
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (0, 'Rua Inhambu, 97 ', 'Rua', 'Moema', 'São Paulo', '04520-010', 'Apartamento', 7000000.0, '2022-06-02'),
        (3, 'Avenida Braz Leme, 1981', 'Avenida', 'Santana', 'São Paulo', '02022-010', 'Apartamento', 1800000.0, '2014-10-27')
    ]
    mock_connect_db.return_value = mock_conn
    
    # WHEN/WANN
    response = client.get('/imoveis/tipo/Apartamento')
    
    # THEN/DANN
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'imoveis' in response_data
    assert '_links' in response_data
    assert len(response_data['imoveis']) == 2
    assert response_data['imoveis'][0]['tipo'] == 'Apartamento'
    assert response_data['imoveis'][1]['tipo'] == 'Apartamento'
    for imovel in response_data['imoveis']:
        assert '_links' in imovel
    
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM imoveis WHERE tipo = %s", 
        ("Apartamento",)
    )

@patch("utils.connect_db")
def test_get_imoveis_filtro_cidade_rota_separada(mock_connect_db, client):
    """Testa filtragem por uma rota separada"""
    
    # GIVEN/GEGEBEN
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Rua Nascimento Silva, 107', 'Rua', 'Ipanema', 'Rio de Janeiro', '22421-025', 'Casa', 5000000.0, '1974-01-25')
    ]
    mock_connect_db.return_value = mock_conn
    
    # WHEN/WANN
    response = client.get('/imoveis/cidade/Rio de Janeiro')
    
    # THEN/DANN
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'imoveis' in response_data
    assert '_links' in response_data
    assert len(response_data['imoveis']) == 1
    assert response_data['imoveis'][0]['cidade'] == 'Rio de Janeiro'
    for imovel in response_data['imoveis']:
        assert '_links' in imovel
    
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM imoveis WHERE cidade = %s", 
        ("Rio de Janeiro",)
    )
