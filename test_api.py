import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db


@pytest.fixture
def client():
    """Cliente de teste para a API. Ele simula um usuário da API de imóveis."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# GET - Todos os imóveis + atributos
@patch("api.connect_db")  # Substitui-se a função que conecta ao banco por um Mock
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

# GET - Imóvel por ID  com suas características concernentes
@patch("api.connect_db")
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