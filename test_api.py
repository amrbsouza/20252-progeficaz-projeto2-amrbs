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
    expected_response = {
        'imoveis': [
            {
                'id': 0,
                'logradouro': 'Rua Inhambu, 97 ',
                'tipo_logradouro': 'Rua',
                'bairro': 'Moema',
                'cidade': 'São Paulo',
                'cep': '04520-010',
                'tipo': 'Apartamento',
                'valor': 7000000.0,
                'data_aquisicao': '2022-06-02'
            },
            {
                'id': 1,
                'logradouro': 'Rua Nascimento Silva, 107',
                'tipo_logradouro': 'Rua',
                'bairro': 'Ipanema',
                'cidade': 'Rio de Janeiro',
                'cep': '22421-025',
                'tipo': 'Casa',
                'valor': 5000000.0,
                'data_aquisicao': '1974-01-25'
            },
            {
                'id': 2,
                'logradouro': 'Praça dos Três Poderes',
                'tipo_logradouro': 'Praça',
                'bairro': 'Centro',
                'cidade': 'Brasília',
                'cep': '70175-900',
                'tipo': 'Palácio',
                'valor': 200000000.0,
                'data_aquisicao': '1960-04-21'
            },
            {
                'id': 3,
                'logradouro': 'Avenida Braz Leme, 1981',
                'tipo_logradouro': 'Avenida',
                'bairro': 'Santana',
                'cidade': 'São Paulo',
                'cep': '02022-010',
                'tipo': 'Apartamento',
                'valor': 1800000.0,
                'data_aquisicao': '2014-10-27'
            }
        ]
    }
    assert response.get_json() == expected_response


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
        'data_aquisicao': '1974-01-25'
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
        'data_aquisicao': '1968-02-15'
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
        'data_aquisicao': '1974-01-25'
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
